from os import stat
import types
from .types import FunctionInfo
from .bucket.CorrosiveBucket import CorrosiveBucket
from .setting import Settings
from typing import List, Dict, Tuple
import ast
import importlib.util

corrosive_buckets: Dict[str, CorrosiveBucket] = {"bucket_std": CorrosiveBucket()}

class CorrosiveRunner:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.modules = {}
        self.pool = []

        for sut in self.settings.systems_under_test:
            try:
                with open(sut.entrypoint, 'r') as file:
                    smoke_tree = ast.parse(file.read())
                    corroz_functions, tree = CorrosiveRunner.parse_ast_tree(smoke_tree)
                    module = CorrosiveRunner.load_in_memory_module(tree, sut.name)
                    self.modules[sut.name] = module

            except Exception as e:
                print(f"Couldn't scan file {sut.entrypoint}. Make sure you are executing acidrunner from the correct directory \nError:\n {e}")
                break
        
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
                if node.name.startswith("_corroz"):
                    args = [arg.arg for arg in node.args.args]
                    corroz_functions.append(FunctionInfo(node.name, filenames, args))
                if bucket_name:
                    # Inject 'await wait_for_token(bucket_name)' at the start of the function
                    wait_for_token_call = ast.Expr(
                        value=ast.Await(
                            value=ast.Call(
                                func=ast.Attribute(
                                    value=ast.Name(id='CorrosivePool', ctx=ast.Load()),
                                    attr='wait_for_token',
                                    ctx=ast.Load()
                                ),
                                args=[ast.Constant(value=bucket_name)],
                                keywords=[]
                            )
                        )
                    )

                    node.body.insert(0, wait_for_token_call)
                    print(f"Injected wait_for_token for function: {node.name} with bucket: {bucket_name}")

                        # Ensure the AST tree is of type ast.Module
        if not isinstance(tree, ast.Module):
            tree = ast.Module(body=tree.body, type_ignores=[])

        return corroz_functions, tree
    
    @staticmethod
    async def wait_for_token(bucket_name: str): 
        global corrosive_buckets
        bucket = corrosive_buckets.get(bucket_name)
        if bucket:
            _ = await bucket.wait_for_tokens()
    
    @staticmethod
    def load_in_memory_module(modified_tree: ast.Module, module_name: str) -> types.ModuleType:
        compiled_code = compile(modified_tree, filename="<ast>", mode="exec")
        module = types.ModuleType(module_name)
        spec = importlib.util.spec_from_loader(module_name, loader=None)
        module.__spec__ = spec

        exec(compiled_code, module.__dict__)

        return module
