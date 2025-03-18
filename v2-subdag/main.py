import os

from kfp import dsl
from kfp.dsl.pipeline_config import PipelineConfig

# Pipeline-level configuration
config = PipelineConfig()
config.set_pipeline_ttl(60)

@dsl.component
def core_comp(dataset: dsl.Output[dsl.Dataset]):
    with open(dataset.path, 'w') as f:
        f.write('foo')


@dsl.component
def crust_comp(input: dsl.Dataset):
    with open(input.path, 'r') as f:
        print('input: ', f.read())


@dsl.pipeline
def core() -> dsl.Dataset:
    task = core_comp()
    task.set_caching_options(False)

    return task.output


@dsl.pipeline
def mantle() -> dsl.Dataset:
    dag_task = core()
    dag_task.set_caching_options(False)

    return dag_task.output


@dsl.pipeline(name=os.path.basename(__file__).removesuffix('.py') + '-pipeline', pipeline_config=config)
#@dsl.pipeline(name=os.path.basename(__file__).removesuffix('.py') + '-pipeline')
def crust():
    dag_task = mantle()
    dag_task.set_caching_options(False)

    task = crust_comp(input=dag_task.output)
    task.set_caching_options(False)
