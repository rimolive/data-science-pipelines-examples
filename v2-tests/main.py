from kfp import compiler
from kfp import dsl
from kfp.dsl import component

@component
def test_step(message: str) -> str:
    return "test"

@dsl.pipeline
def test_pipeline():
    pre_step = test_step(message="pre")
    # Replacing input with a static import works.
    # Using dsl.Inputs/dsl.Outputs causes the same issue. 
    exit_step = test_step(message=pre_step.output)
    with dsl.ExitHandler(exit_task=exit_step):
        test_step(message="test")


compiler.Compiler().compile(test_pipeline, "test_pipeline.yaml")