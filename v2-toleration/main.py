import kfp
from kfp import dsl
from kfp import kubernetes

@dsl.component()
def echo_message(message: str) -> None:
    import subprocess
    subprocess.run(["echo", message])


@dsl.pipeline(
    name="demo pipeline",
    description="A demo pipeline that prints to stdout"
)
def sequential_pipeline(message: str = "Hello world with timeout!"):
    hello_world_operator = echo_message(message=message)
    hello_world_operator.set_cpu_request(cpu="1")
    hello_world_operator.set_memory_request(memory="4Gi")
    hello_world_operator.set_memory_limit(memory="4Gi")

    kubernetes.add_toleration(
        task=hello_world_operator,
        key='toleration_key',
        operator='Equal',  # 'Equal' | 'Exists' | None = None
        value='true',
        effect='NoSchedule',
    )


if __name__ == '__main__':
    kfp.compiler.Compiler().compile(
        pipeline_func=sequential_pipeline,
        package_path=__file__ + '.yaml',
    )