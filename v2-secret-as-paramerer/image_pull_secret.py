

from kfp import dsl
from kfp import kubernetes, compiler

from kfp import dsl
from kfp import kubernetes
from kfp.dsl import Output, OutputPath


@dsl.component(base_image="quay.io/opendatahub/ds-pipelines-ci-executor-image:v1.0")
def some_component():
    print("mounted")

@dsl.pipeline
def my_pipeline(pull_secret_1: str, pull_secret_2: str):
    task = some_component()
    task.set_caching_options(enable_caching=False)
    kubernetes.set_image_pull_secrets(
        task,
        secret_names=[pull_secret_1, pull_secret_2])


compiler.Compiler().compile(
    pipeline_func=my_pipeline,
    package_path=__file__.replace('.py', '.yaml'))