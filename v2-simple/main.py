from kfp import dsl
from kfp import compiler
from kfp import kubernetes
from kfp.dsl import Output,Dataset

@dsl.component(packages_to_install=["pandas"])
def read_data(data: Output[Dataset]):
    import pandas as pd
    df = pd.read_csv('sample.csv')
    
    with open(data.path, 'w') as f:
        df.to_csv(f)


@dsl.pipeline
def my_pipeline():
    """My ML pipeline."""
    read_data_op = read_data()
    read_data_op.outputs['data']

    # kubernetes.mount_pvc(read_data, pvc_name="data-rw", mount_path="/data-rw")
    # return read_data().output

compiler.Compiler().compile(my_pipeline, package_path='pipeline.yaml')
