import os

from kfp import dsl
from kfp import compiler
from kfp.dsl.pipeline_config import PipelineConfig

@dsl.component()
def hello_world(text: str) -> str:
    print(text)
    return text

@dsl.component()
def exit_pipeline():
    print("Exiting...")

config = PipelineConfig()
config.set_ttl(60)

@dsl.pipeline(name='hello-world', description='A simple intro pipeline', pipeline_config=config)
def pipeline_hello_world(text: str = 'hi there'):
    """Pipeline that passes small pipeline parameter string to consumer op."""

    # consume_task = hello_world(
    #     text=text)  # Passing pipeline parameter as argument to consumer op
    exit = exit_pipeline()

    with dsl.ExitHandler(exit):
        hello_world(text=text)