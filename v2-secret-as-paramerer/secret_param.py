from kfp import dsl
from kfp import kubernetes, compiler

from kfp import dsl
from kfp import kubernetes
from kfp.dsl import Output, OutputPath


@dsl.component(base_image="quay.io/opendatahub/ds-pipelines-ci-executor-image:v1.0")
def some_component(this_is_a_comp_input_arg: str):
    import os
    username = os.getenv("USERNAME_VAR", "didn't work")
    psw = os.getenv("PASSWORD_VAR", "didn't work")
    psw2 = os.getenv("PASSWORD_VAR2", "didn't work")
    print("PRINTING ENV VARS:")
    print("username:", username)
    print("psw: ", psw)
    print("psw2: ", psw2)


@dsl.component(base_image="quay.io/opendatahub/ds-pipelines-ci-executor-image:v1.0")
def generate_secret_name(some_output: OutputPath(str)):
    secret_name = "another-secret-test"
    with open(some_output, 'w') as f:
        f.write(secret_name)


@dsl.pipeline
def my_pipeline(secret_parm: str, comp_pipeline_input: str):
    task = some_component(this_is_a_comp_input_arg=comp_pipeline_input)
    kubernetes.use_secret_as_env(
        task,
        secret_name='my-secret',
        secret_key_to_env={'username': 'USERNAME_VAR'})
    kubernetes.use_secret_as_env(
        task,
        secret_name=secret_parm,
        secret_key_to_env={'password': 'PASSWORD_VAR'})

    task2 = generate_secret_name()
    kubernetes.use_secret_as_env(
        task,
        secret_name=task2.output,
        secret_key_to_env={'password': 'PASSWORD_VAR2'})


compiler.Compiler().compile(
    pipeline_func=my_pipeline,
    package_path=__file__.replace('.py', '.yaml'))