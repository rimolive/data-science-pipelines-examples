import kfp
from kfp import dsl


@dsl.component
def cpu_limit() -> str:
    return "4000m"


@dsl.component
def sum_numbers(a: int, b: int) -> int:
    return a + b


@dsl.pipeline
def pipeline():
    sum_numbers_task = sum_numbers(a=1, b=2)
    sum_numbers_task.set_cpu_limit(cpu_limit().output)


kfp.compiler.Compiler().compile(
    pipeline_func=pipeline,
    package_path="test.json",
)