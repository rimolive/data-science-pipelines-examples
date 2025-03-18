

from kfp import dsl
from kfp import kubernetes, compiler

from kfp import dsl
from kfp import kubernetes
from kfp.dsl import Output, OutputPath


@dsl.component(base_image="quay.io/opendatahub/ds-pipelines-ci-executor-image:v1.0")
def some_component():
    print("mounted")




@dsl.pipeline
def my_pipeline(node_selector_input: dict):
    task = some_component()
    task.set_caching_options(enable_caching=False)

    kubernetes.add_node_selector(
        task,
        label_key="disk-type",
        label_value="us-west"
    )

    # # Runtime Constant
    # node_selector = {
    #     "disk-type": "ssd4",
    #     "region": "us-west4",
    # }
    # kubernetes.add_node_selector(
    #     task,
    #     node_selector_json=node_selector,
    # )

    # Component Input
    kubernetes.add_node_selector(
        task,
        node_selector_json=node_selector_input,
    )
    kubernetes.add_node_selector(
        task,
        label_key="disk-type2",
        label_value="us-west2"
    )
    kubernetes.add_node_selector(
        task,
        label_key="disk-type3",
        label_value="us-west3"
    )


compiler.Compiler().compile(
    pipeline_func=my_pipeline,
    package_path=__file__.replace('.py', '.yaml'))