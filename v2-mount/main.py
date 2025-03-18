import kfp
from kfp.kubernetes import mount_pvc
from kfp.dsl import component

@component
def test_component(greeting: str = "World"):
    print(f"Hello {greeting}")

@kfp.dsl.pipeline(name='pvc mounting pipeline')
def test_pipeline_fail(
    pvc_name: str = 'pcv-name',
    greeting: str = "World"
):
    test_task = test_component(greeting=greeting)
    mount_pvc(test_task, 'pvc', '/mnt/pipeline')

@kfp.dsl.pipeline(name='pvc mounting pipeline')
def test_pipeline_pass(
    pvc_name: str = 'pcv-name',
    greeting: str = "World"
):
    test_task = test_component()
    mount_pvc(test_task, 'pvc', '/mnt/pipeline')
    
if __name__ == '__main__':
    kfp.compiler.Compiler().compile(test_pipeline_fail, 'test_pipeline_fail.yaml')
    kfp.compiler.Compiler().compile(test_pipeline_pass, 'test_pipeline_pass.yaml')
