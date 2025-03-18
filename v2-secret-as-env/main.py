from kfp import dsl
from kfp import kubernetes

@dsl.component(base_image="python:3.10")
def print_secret():
    with open('/mnt/my_vol') as f:
        print(f.read())

@dsl.pipeline
def pipeline():
    task = print_secret()
    kubernetes.use_secret_as_volume(task,
                                    secret_name='my-secret',
                                    mount_path='/mnt/my_vol')
    kubernetes.set_timeout(task, 160)