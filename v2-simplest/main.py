from kfp import dsl
from kfp import compiler

@dsl.component(base_image="quay.io/opendatahub/ds-pipelines-sample-base:v1.0")
def test():
    print("Hello")

@dsl.pipeline(name="test", description="Test")
def test_pipeline():
    test()

compiler.Compiler().compile(test_pipeline, package_path="test.yaml")