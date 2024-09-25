# AcidRunner

AcidRunner is a benchmarking/testing framework designed for testing and
benchmarking APIs with a focus on LLM APIs. I use it to test chains of 
prompts. But you could just as well test it to stress test APIs. Or use
it to generate synthetic data.

For now only async tests/benchmarks are supported.

## Features

- **Dynamic Task Loading**: Automatically loads and executes tests based on your Python functions.
- **Rate Limit Injection**: Use a decorator to inject rate-limit code at runtime
- **Task Processing**: Corrosive task results are collected, processed, and written to a sqlite db
- **Highly Configurable**: Define systems under test, entry points, rate limits, and file output locations via configuration files.
- **Typer CLI Integration**: Simple CLI interface to run benchmarks and define parameters.

## Installation

To install the package, run the following command:

```bash
pip install -e .
```

## Usage
1. Configure the Acidfile.yaml

The `Acidfile.yaml` file defines the systems under test (SUT) and other settings:

```yaml
systems_under_test:
  - name: 4-turbo-vs-4o-test-data-extraction-capabilities
    entrypoint: /path/to/your/entry_point.py

  - name: generate-new-test-cases-on-auto-mode
    entrypoint: ./auto_cases.py

buckets:
  - name: bucket_groq
    rpm: 30
  - name: bucket_openai
    rpm: 1000
  - name: bucket_slow_custom
    rpm: 10
  - name: bucket_fast_custom
    rpm: 100000

file_settings:
  - data_dir: /path/to/data_dir/
  - sqlite_enable: true
```

- systems_under_test: Define the SUTs by name and entry points (Python files to scan for corrosive tasks).
- buckets: Define rate limits for your systems, in requests per minute (RPM).
  - You can mark any function in your test file with a decorator `@use_bucket('bucket_name')` it will inject the rate limiter at runtime
- file_settings: Set the directory where output files should be saved and enable SQLite if necessary.

2. Create benchmarks/tests:

```python
from acidrunner.decorators import use_bucket, in_files
from acidrunner.types.types_custom import AcidBoolResult

@use_bucket('bucket_1')
@in_files(['bool_tests.yaml'])
async def _bench_pushed_to_data_table(query) -> AcidBoolResult:
    api_res = await fetch_transactions(query)

    res = False
    if api_res['generated_text'] == 'Answer pushed to data table!':
        res = True

    return AcidBoolResult(res, meta_data={"api_data": api_res})
```

The names of the functions that you want to be executed by AcidRunner
should start with `_bench`. As you can see the test here is marked with
a bucket called bucket_1. But you can mark any function in the file with
a `@use_bucket("bucketname")` in case your test executes multiple API calls
in succession. 


And the decorator `@in_files(['tests.yaml'])` is a
decorator that takes a `List` of files containing yaml data you want to
run against the test. You can only use this decorator with functions
marked with \_bench. 

`_bench` functions can return `Any` but if you want AcidRunner to
actually do something with the result you should return one of the following
types:

```
@dataclass
class AcidBoolResult:
    result: bool
    meta_data: Dict

@dataclass
class AcidFloatResult:
    result: float 
    meta_data: Dict
    a_range: Tuple[float, float] = (0.0, 1.0)

@dataclass
class AcidCosineResult:
    buffer1: List[float]
    buffer2: List[float]
    meta_data: Dict 
    a_range: Tuple[float, float] = (0.0, 1.0)
```

- The `AcidBoolResult` is just a bool and an extra metadata Dict with data that
you want to store. When it's True AcidRunner will count the test as
successful. 
- The `AcidFloatResult` has a float as result and an accepted range,
  when the float is within the range AcidRunner will count the test as
  successful. 
- The `AcidCosineResult` contains two buffers each containing a Vector
  Embedding. AcidRunner will check if the Cosine Similarity score is
  within the range you have specified in `a_range`.

In the future I want to implement an `AcidCosineStringResult` that makes
it so you don't need to calculate the similarity in your tests but the
runner will do it for you.


3. Set up the base cases (tests.yaml):
``` yaml
tests:
  - name: "filter_transactions_above_500"
    args:
      query: "Can you filter transactions above 500?"

  - name: "scan_transactions_above_500"
    args:
      query: "Can you scan for transactions above 500?"

  - name: "show_highest_transactions"
    args:
      query: "What are the highest transactions?"

  - name: "list_above_500"
    args:
      query: "Can you list tansactions above 500"
```

As you can see you can specify the name of the test case and the
arguments that should be sent to the function. This makes the system
very flexible.

4. Run the tests/benchmarks
Use the provided CLI interface to run the benchmark with the desired number of runs:

```bash
python -m acidrunner run -f /path/to/Acidfile.yaml -r 10
```
-f: Path to the configuration file. If you are in the same directory as your Acidfile.yaml there is no need to specify this.
-r: Number of times all your tests/benchmark will execute.

## Meta Data:

There are certain keys in the meta_data Dict in the AcidResults that are
used in the CorrosiveRunner. For now only `write_to_yaml` is
implemented. Todo: HTTP-status code

### meta_data['write_to_yaml']
Let's say you have an AI that generates inputs to fuzz your API
endpoint, and let's say it succeeds in bypassing the security mechanisms
or it manages to trigger an error in the API. You could if you'd like
write the inputs used straight to a new tests.yaml file. For example:

``` python
@in_files(['fuzzy_mala.yaml'])
async def _bench_generate_attack_prompt(model1, model2) -> AcidBoolResult:
    meta_data = {}
    temp = random.randint(100) / 100
    generated_prompt = await malicious_prompt_generator(model1, history, temp)
    hex_code = await prompt_validator(generated_prompt, model2)

    test_passed = False
    if hex_code == "0x01":
        test_passed = True 

    meta_data['output'] = {"attacker": generated_prompt, "defender": hex_code}
    if not test_passed:
        meta_data['write_to_yaml'] = {"name":"fuzzy-generated","args": {"attacker": generated_prompt.strip()}}

    return AcidBoolResult(test_passed, meta_data)
```

As you can see, whenever the test fails it adds the meta_data for
write_to_yaml. The CorrosiveProcessor will see this and when all your
runs are complete it will drop it to a new yaml file in the
`data_dir/yaml_out`


