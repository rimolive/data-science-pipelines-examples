import kfp
from kfp import dsl

import glob
import pandas as pd
import requests
import io
import zipfile
import re

@dsl.component
def ingest_data() -> str:
    return "Ingest Data"

@dsl.component
def preprocess_data(msg: str) -> str:
    return "preprocessed data"

@dsl.component
def train_model_A(msg: str):
    print("Model A")

@dsl.component
def train_model_B(msg: str):
    print("Model B")

@dsl.pipeline(name="pipeline-test")
def world_cup_pipeline():
    ingest_and_process_task = ingest_data()
    preprocess_data_task = preprocess_data(msg=ingest_and_process_task.output)
    train_model_A_task = train_model_A(msg=preprocess_data_task.output)
    train_model_B_task = train_model_B(msg=preprocess_data_task.output)

kfp.compiler.Compiler().compile(
    pipeline_func=world_cup_pipeline,
    package_path= __file__.replace('.py', '-v2.yaml'))
