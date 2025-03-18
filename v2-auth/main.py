import kfp

# the namespace in which you deployed Kubeflow Pipelines
namespace = "kubeflow"

# the KF_PIPELINES_SA_TOKEN_PATH environment variable is used when no `path` is set
# the default KF_PIPELINES_SA_TOKEN_PATH is /var/run/secrets/kubeflow/pipelines/token
credentials = kfp.auth.ServiceAccountTokenVolumeCredentials(path=None)

client = kfp.Client(host=f"http://ml-pipeline-ui.{namespace}", credentials=credentials)

print(client.list_experiments())