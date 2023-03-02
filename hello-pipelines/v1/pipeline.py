import kfp
import kfp.components as components
import kfp.dsl as dsl

import glob
import pandas as pd
import requests
import io
import zipfile
import re

def ingest_data() -> str:
    return "Ingest Data"

def preprocess_data(msg: str) -> str:
    return "preprocessed data"

def train_model_A(msg: str):
    print("Model A")

def train_model_B(msg: str):
    print("Model B")

ingest_data_step = components.create_component_from_func(
    func=ingest_data,
    base_image="registry.redhat.io/ubi8/python-39",
    packages_to_install=['pandas'],)
preprocess_data_step = components.create_component_from_func(
    func=preprocess_data,
    base_image="registry.redhat.io/ubi8/python-39",
    packages_to_install=['pandas'],)
train_model_A_step = components.create_component_from_func(
    func=train_model_A,
    base_image="registry.redhat.io/ubi8/python-39",
    packages_to_install=['pandas'],)
train_model_B_step = components.create_component_from_func(
    func=train_model_B,
    base_image="registry.redhat.io/ubi8/python-39",
    packages_to_install=['pandas'],)

@dsl.pipeline(name="pipeline-test")
def world_cup_pipeline():
    ingest_and_process_task = ingest_data_step()
    preprocess_data_task = preprocess_data_step(ingest_and_process_task.output)
    train_model_A_task = train_model_A_step(preprocess_data_task.output)
    train_model_B_task = train_model_B_step(preprocess_data_task.output)

from kfp_tekton.compiler import TektonCompiler
TektonCompiler().compile(
    pipeline_func = world_cup_pipeline,
    package_path = __file__.replace('.py', '-v1.yaml'))
