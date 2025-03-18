from kfp import dsl
from kfp import kubernetes

@dsl.component
def make_data():
    with open('/data/file.txt', 'w') as f:
        f.write('my data')

@dsl.pipeline
def my_pipeline():
    pvc1 = kubernetes.CreatePVC(
        pvc_name_suffix="-my-pvc",
        access_modes=["ReadWriteOnce"],
        size="5Mi",
        annotations={"foo": "bar"},
    )

    task1 = make_data()

    kubernetes.mount_pvc(
        task1,
        pvc_name=pvc1.outputs['name'],
        mount_path='/data'
    )

