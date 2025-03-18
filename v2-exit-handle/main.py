import os

from kfp import compiler
from kfp import dsl
from kfp import local
from kfp.dsl import component

local.init(local.DockerRunner())

@component
def print_op(message: str):
    """Prints a message."""
    print(message)


@component
def fail_op(message: str):
    """Fails."""
    import sys
    print(message)
    sys.exit(1)


@dsl.pipeline(name='pipeline-with-exit-handler')
def pipeline_exit_handler(message: str = 'Hello World!'):

    exit_task = print_op(message='Exit handler has worked!')

    with dsl.ExitHandler(exit_task):
        print_op(message=message)
        fail_op(message='Task failed.')

# pipeline_exit_handler()