from kfp import dsl
from kfp import kubernetes, compiler

from kfp import dsl
from kfp import kubernetes
from kfp.dsl import Output, OutputPath

@dsl.component(base_image="quay.io/opendatahub/ds-pipelines-ci-executor-image:v1.0")
def some_component():
    print("mounted")


@dsl.pipeline
def my_pipeline(toleration_json: dict):
    task = some_component()
    task.set_caching_options(enable_caching=False)

    kubernetes.add_toleration(
        task,
        toleration_json=toleration_json
    )
    kubernetes.add_toleration(
        task,
        key="key2",
        operator="Equal",
        value="value1",
        effect="NoSchedule",
    )


compiler.Compiler().compile(
    pipeline_func=my_pipeline,
    package_path=__file__.replace('.py', '.yaml'))