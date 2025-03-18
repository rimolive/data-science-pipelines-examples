import kfp
from kfp import dsl
from kfp import kubernetes


@dsl.component
def test_step():
    print("Hello world")


@dsl.pipeline
def test_pipeline():
    pvc1 = kubernetes.CreatePVC(
        access_modes=["ReadWriteOnce"],
        size="10Mi",
        storage_class_name='standard-csi',
    )
    step = test_step().after(pvc1)
    pvc2 = kubernetes.DeletePVC(
        pvc_name=pvc1.outputs['name']).after(step)

