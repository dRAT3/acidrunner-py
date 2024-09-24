from os import stat
import time
import asyncio
import copy
import types
from types_custom import CorrosiveTaskData, CorrosiveTaskDataImmutable, FunctionInfo
from types_custom import AcidBoolResult, AcidFloatResult, AcidCosineResult
from algo.distance import CosineSimilarityBasic
from bucket.CorrosiveBucket import CorrosiveBucket
from setting import Bucket, Settings, yaml
from typing import List, Dict, Tuple, Optional
import ast
import importlib.util
from uuid import uuid4
import sys

corrosive_buckets: Dict[str, CorrosiveBucket] = {"bucket_std": CorrosiveBucket()}

class CorrosiveRunner:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.modules = {}
        self.pool = []
        self.semaphore = asyncio.Semaphore(12)

        for sut in self.settings.systems_under_test:
            try:
                with open(sut.entrypoint, 'r') as file:
                    smoke_tree = ast.parse(file.read())
                    corroz_functions, tree = CorrosiveRunner.parse_ast_tree(smoke_tree)
                    module = CorrosiveRunner.load_in_memory_module(tree, sut.name)
                    self.modules[sut.name] = module
                    for corro in corroz_functions:
                        self.funcinfo_to_pool(corro, sut.name)

                    CorrosiveRunner.setup_buckets(self.settings.buckets)

            except Exception as e:
                print(f"Couldn't scan file {sut.entrypoint}. Make sure you are executing acidrunner from the correct directory \nError:\n {e}")
                sys.exit(0x00)
        
    @staticmethod
    def parse_ast_tree(tree) -> Tuple[List[FunctionInfo], ast.Module]:
        """"""
        print("Parsing ast tree")
        corroz_functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith("_corroz"):
                print(f"Found non async _corroz skipping (not supported): {node.name}")

            elif isinstance(node, ast.AsyncFunctionDef):
                filenames = None
                bucket_name = None
                print(f"Found function checking for decorators: {node.name}")
                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Call) and hasattr(decorator.func, 'id'):
                        if decorator.func.id == 'use_bucket': 
                            bucket_name = decorator.args[0].s if decorator.args else None
                        elif decorator.func.id == 'in_files':
                            filenames = [arg.s for arg in decorator.args[0].elts] if decorator.args else []
                if node.name.startswith("_bench"):
                    args = [arg.arg for arg in node.args.args]
                    corroz_functions.append(FunctionInfo(node.name, filenames, args))
                if bucket_name:
                    # Inject 'await wait_for_token(bucket_name)' at the start of the function
                    wait_for_token_call = ast.Expr(
                        value=ast.Await(
                            value=ast.Call(
                                func=ast.Attribute(
                                    value=ast.Name(id='CorrosiveRunner', ctx=ast.Load(), lineno=node.lineno, col_offset=node.col_offset),
                                    attr='wait_for_token',
                                    ctx=ast.Load(),
                                    lineno=node.lineno,  # Setting the line number
                                    col_offset=node.col_offset  # Setting the column offset
                                ),
                                args=[ast.Constant(value=bucket_name, lineno=node.lineno, col_offset=node.col_offset)],
                                keywords=[],
                                lineno=node.lineno,
                                col_offset=node.col_offset
                            ),
                            lineno=node.lineno,
                            col_offset=node.col_offset
                        ),
                        lineno=node.lineno,
                        col_offset=node.col_offset
                    )

                    node.body.insert(0, wait_for_token_call)
                    print(f"Injected wait_for_token for function: {node.name} with bucket: {bucket_name}")

        # Ensure the AST tree is of type ast.Module
        if not isinstance(tree, ast.Module):
            tree = ast.Module(body=tree.body, type_ignores=[])

        return corroz_functions, tree
    
    @staticmethod
    def load_in_memory_module(modified_tree: ast.Module, module_name: str) -> types.ModuleType:
        compiled_code = compile(modified_tree, filename="<ast>", mode="exec")
        module = types.ModuleType(module_name)
        spec = importlib.util.spec_from_loader(module_name, loader=None)
        module.__spec__ = spec

        exec(compiled_code, module.__dict__)

        return module

    @staticmethod
    def setup_buckets(buckets: List[Bucket]):
        for buck in buckets:
            tok_buck = CorrosiveBucket(buck.rpm, buck.rpm/60)
            global corrosive_buckets
            corrosive_buckets[buck.name] = tok_buck

    def funcinfo_to_pool(self, func_info: FunctionInfo, sut_name: str):
        for file in func_info.filenames:
            with open(file, 'r') as file:
                yaml_data = yaml.safe_load(file)
                for corro in yaml_data['tests']:
                    task_data_immutable = CorrosiveTaskDataImmutable(
                        task_id = str(uuid4()),
                        name = corro['name'],
                        func=func_info,
                        args = [corro['args'][arg] for arg in corro['args']],
                        sut_name=sut_name,
                    )
                    task_data = CorrosiveTaskData(
                           immutable=task_data_immutable,
                            meta_data={},
                            result=None
                    )
                    tc = copy.deepcopy(task_data)
                    self.pool.append(tc)

    @staticmethod
    async def wait_for_token(bucket_name: str): 
        global corrosive_buckets
        bucket = corrosive_buckets.get(bucket_name)
        if bucket:
            _ = await bucket.wait_for_tokens()

    async def run_wrapped_tasks(self, run: int) -> List[Optional[CorrosiveTaskData]]:
        async def wrapped_task(coro_task):
            async with self.semaphore:
                return await self.__run_corrosive_task(coro_task)
        
        print(f"Starting run {run}:")
        t0 = time.time_ns()
        coroutines = [wrapped_task(coro_task) for coro_task in self.pool]
        results = await asyncio.gather(*coroutines)
        elapsed = (time.time_ns() - t0) / 1_000_000_000
        print(f"Run {run} executed in {elapsed} seconds")

        return results

    async def __run_corrosive_task(self, coro_task: CorrosiveTaskData):
        module = self.modules[coro_task.immutable.sut_name]

        if hasattr(module, coro_task.immutable.func.function_name):
            func = getattr(module, coro_task.immutable.func.function_name)
            try:
                t0 = time.time_ns()
                res = await func(*coro_task.immutable.args)
                coro_task.elapsed = time.time_ns() - t0
                coro_task.meta_data = res.meta_data
                coro_task.result = res

                if type(res) == AcidBoolResult:
                    coro_task.succes = res.result 
                elif type(res) == AcidCosineResult:
                    score = CosineSimilarityBasic.calculate(coro_task.result.result.buffer1, coro_task.result.result.buffer2)
                    coro_task.succes = CosineSimilarityBasic.is_in_range(score, coro_task.result.a_range)
                elif type(res) == AcidFloatResult:
                    coro_task.succes = CosineSimilarityBasic.is_in_range(coro_task.result, coro_task.result.a_range)

                print(f"[{coro_task.immutable.name}][{coro_task.immutable.func.function_name}]:")
                print(f"{coro_task.immutable.task_id}")
                print(f"{coro_task.immutable.args}")
                print(f"Test passed: {coro_task.result}")
                print(f"Meta_Data: {coro_task.meta_data}")

                coro_task.executed = True
                
                return copy.deepcopy(coro_task) # Test if second deepcopy necessary

            except Exception as e:
                print(f"Error executing func {e}")
        else:
            print(f"Function {coro_task.immutable.func.function_name} not found in module {module.__name__}")

    async def run(self, runs: int) -> List[List[Optional[CorrosiveTaskData]]]:
        return [await self.run_wrapped_tasks(i) for i in range(runs)]

    ###Todo: All runs at once

if __name__=="__main__":
    settings = Settings.load_settings("./demo/fuzzy_mala/Acidfile.yaml")
    runner = CorrosiveRunner(settings)

    _ = asyncio.run(runner.run(1))

