from kfp import dsl
from kfp import kubernetes

@dsl.component
def check_sdg_only() -> bool:
    import os

    sdg_only = False
    if os.environ["SDG_ONLY"] == "true":
        sdg_only = True

    return sdg_only

@dsl.component
def print_msg(msg: str):
    print(msg)

@dsl.pipeline
def conditional_test():
    check_sdg_only_op = check_sdg_only()
    check_sdg_only_op.set_caching_options(False)
    kubernetes.use_config_map_as_env(
        check_sdg_only_op,
        config_map_name="cm-test",
        config_map_key_to_env={"SDG_ONLY": "SDG_ONLY"})
    
    with dsl.If(check_sdg_only_op.output == True):
        print_msg(msg='Foo')
    with dsl.Else():
        print_msg(msg='Bar')