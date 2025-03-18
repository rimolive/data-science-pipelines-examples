from kfp import dsl
from kfp import kubernetes, compiler

from kfp import dsl
from kfp import kubernetes
from kfp.dsl import Output, OutputPath


@dsl.component(base_image="quay.io/opendatahub/ds-pipelines-ci-executor-image:v1.0")
def some_component():
    import os
    username = os.getenv("USERNAME_VAR", "didn't work")
    psw = os.getenv("PASSWORD_VAR", "didn't work")
    print("PRINTING ENV VARS:")
    print("username:", username)
    print("psw: ", psw)


@dsl.component(base_image="quay.io/opendatahub/ds-pipelines-ci-executor-image:v1.0")
def some_component2():
    import os
    psw2 = os.getenv("PASSWORD_VAR2", "didn't work")
    print("psw2: ", psw2)

@dsl.component(base_image="quay.io/opendatahub/ds-pipelines-ci-executor-image:v1.0")
def generate_configmap_name(some_output: OutputPath(str)):
    configmap_name = "another-configmap-test"
    with open(some_output, 'w') as f:
        f.write(configmap_name)


@dsl.pipeline
def my_pipeline(configmap_parm: str):
    task = some_component().set_caching_options(enable_caching=False)
    kubernetes.use_config_map_as_env(
        task,
        config_map_name='my-configmap',
        config_map_key_to_env={'username': 'USERNAME_VAR'})
    kubernetes.use_config_map_as_env(
        task,
        config_map_name=configmap_parm,
        config_map_key_to_env={'password': 'PASSWORD_VAR'})

    task2 = some_component2().set_caching_options(enable_caching=False)
    task3 = generate_configmap_name().set_caching_options(enable_caching=False)
    kubernetes.use_config_map_as_env(
        task2,
        config_map_name=task3.output,
        config_map_key_to_env={'password': 'PASSWORD_VAR2'})


compiler.Compiler().compile(
    pipeline_func=my_pipeline,
    package_path=__file__.replace('.py', '.yaml'))