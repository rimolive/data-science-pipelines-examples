from typing import List

from kfp import dsl
from kfp.dsl import component


@component(base_image="python:3.10-slim")
def custom_dummy_op() -> str:
    return "dummy"


@component(base_image="python:3.10-slim-buster")
def run_step(message: list, step: int = 1) -> bool:
    return step in message


@component(base_image="python:3.11.3-slim-buster")
def list_to_json(data: list) -> str:
    import json

    return json.dumps(data)


@dsl.pipeline(name="inference-pipeline")
def inference_pipeline(
        steps: List[int], entity: str, pipeline_mode: str, run_mode: str, models: List[str]
):
    """
    Args:
    Returns:
    """

    step1_run = run_step(message=steps, step=1).set_display_name("RUN 1")
    step2_run = run_step(message=steps, step=2).set_display_name("RUN 2")
    step3_run = run_step(message=steps, step=3).set_display_name("RUN 3")

    "STEP 1"
    with dsl.ExitHandler(
            exit_task=custom_dummy_op().set_display_name("EXIT TASK 1"), name="EXIT STEP 1"
    ) as e1:
        with dsl.If(step1_run.output == True, name="Run Step 1?"):
            custom_dummy_op().set_display_name("Running step 2")

    "STEP 2"
    step2_run.after(e1)

    with dsl.ExitHandler(
            exit_task=custom_dummy_op().set_display_name("EXIT TASK 2"), name="EXIT STEP 2"
    ) as e2:
        with dsl.If(step2_run.output == True, name="Run Step 2?"):
            with dsl.ParallelFor(
                    list_to_json(data=models).output,
                    name="Run Model Scoring",
                    parallelism=2,
            ) as model_run:  # noqa
                custom_dummy_op().set_display_name("RUN MICKY'S COMPONENT HERE")

    "STEP 3"
    step3_run.after(e2)

    with dsl.ExitHandler(
            exit_task=custom_dummy_op().set_display_name("EXIT TASK 3"), name="EXIT STEP 3"
    ):
        with dsl.If(step3_run.output == True, name="Run Step 3?"):
            custom_dummy_op().set_display_name("Running step 3")
