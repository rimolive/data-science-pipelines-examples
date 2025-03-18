from kfp import dsl
from kfp import kubernetes

@dsl.component
def read_data():
    with open('/reused_data/file.txt') as f:
        print(f.read())

@dsl.pipeline
def my_snapshot_pipeline():
    pvc2 = kubernetes.CreatePVC(
        pvc_name_suffix="-foo",
        access_modes=["ReadWriteOnce"],
        size="1Gi",
        storage_class_name="standard-csi"
        # data_source={"api_group": "snapshot.storage.k8s.io",
        #     "kind": "VolumeSnapshot",
        #     "name": "my-pvc-snapshot",
        # },
    )

    task2 = read_data()

    kubernetes.mount_pvc(
        task2,
        pvc_name=pvc2.outputs['name'],
        mount_path='/reused_data',
    )
