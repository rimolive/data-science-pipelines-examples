from kfp import dsl
from kfp import kubernetes

@dsl.component(base_image="quay.io/rmartine/python:3.9-alpine")
def test_secret_as_env():
    import os

    print(os.environ['SECRET_VAR'])

@dsl.component(base_image="quay.io/rmartine/python:3.9-alpine")
def test_secret_as_volume():
    with open("/tmp/test/ca.crt") as f:
        print(f.readline())

@dsl.component(base_image="quay.io/rmartine/python:3.9-alpine")
def test_cm_as_env():
    import os

    print(os.environ['CM_VAR'])

@dsl.component(base_image="quay.io/rmartine/python:3.9-alpine")
def test_cm_as_volume():
    with open("/tmp/test/ca.crt") as f:
        print(f.readline())

@dsl.pipeline
def secret_as_parameter(secret_name: str, cm_name: str):
    first_op = test_secret_as_env()
    kubernetes.use_secret_as_env(first_op, secret_name, secret_key_to_env={'password': 'SECRET_VAR'})

    second_op = test_secret_as_volume()
    kubernetes.use_secret_as_volume(second_op, secret_name, mount_path="/tmp/test")

    third_op = test_cm_as_env()
    kubernetes.use_config_map_as_env(third_op, cm_name, config_map_key_to_env={'testing': 'CM_VAR'})

    fourth_op = test_cm_as_volume()
    kubernetes.use_config_map_as_volume(fourth_op, cm_name, mount_path="/tmp/test")