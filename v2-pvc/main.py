from kfp import dsl
from kfp import kubernetes


@dsl.pipeline
def my_pipeline():
    pvc = kubernetes.CreatePVC(
        pvc_name_suffix="-my-pvc",
        access_modes=["ReadWriteOnce"],
        size="5Mi",
        annotations={"foo": "bar"},
    )

    kubernetes.DeletePVC(
        pvc_name=pvc.outputs['name']
    ).after(pvc)