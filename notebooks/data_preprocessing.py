# Databricks notebook source

# %pip install -e ..
# %restart_python

# COMMAND ----------
# from pathlib import Path
# import sys
# sys.path.append(str(Path.cwd().parent / 'src'))

# COMMAND ----------
import pandas as pd
import yaml
from loguru import logger
from pyspark.sql import SparkSession

from diabetes_process.config import ProjectConfig


config = ProjectConfig.from_yaml(config_path="../projec_config_diabetes.yml", env="dev")

logger.info("Configuration loaded:")
logger.info(yaml.dump(config, default_flow_style=False))
# COMMAND ----------
spark = SparkSession.builder.getOrCreate()
filepath = "../data/diabetes.csv"

# Load the data
df = pd.read_csv(filepath)
# COMMAND ----------
display(df)
# COMMAND ----------
