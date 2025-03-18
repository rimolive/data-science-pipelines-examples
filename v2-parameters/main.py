import kfp.dsl as dsl
from kfp import compiler
# execute Ray jobs
@dsl.component(base_image="python:3.10")
def execute_ray_job(
   params: dict,
):
  print(f"in execute_ray_job")


  # Pipeline to invoke execution on remote resource
@dsl.pipeline(
    name="dummy-pipeline",
    description="",
)
def dummy_pipeline(
    iterations: dict
):
   execute_job = execute_ray_job(
       params=iterations,
   )
if __name__ == "__main__":
   # Compiling the pipeline
   compiler.Compiler().compile(dummy_pipeline, __file__.replace(".py", ".yaml"))