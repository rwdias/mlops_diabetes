"""Data preprocessing module for diabetes database"""

import time
import numpy as np
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, to_utc_timestamp
from sklearn.model_selection import train_test_split
from diabetes_process import ProjectConfig


class DataProcessing:
    """This class is responsible for data issues."""

    def __init__(
        self,
        pandas_df: pd.DataFrame,
        config: ProjectConfig,
        spark: SparkSession
    ) -> None:
        self.df = pandas_df
        self.config = config
        self.spark = spark

    def preprocess(self) -> None:
        cat_features = self.config.cat_features
        num_features = self.config.num_features
        target = self.config.target

        # Remover outliers usando IQR
        mask = pd.Series(True, index=self.df.index)

        for feature in num_features:
            q1 = self.df[feature].quantile(0.25)
            q3 = self.df[feature].quantile(0.75)
            iqr = q3 - q1

            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            feature_mask = (
                (self.df[feature] >= lower_bound)
                & (self.df[feature] <= upper_bound)
            )

            mask = mask & feature_mask

        initial_rows = len(self.df)

        self.df = self.df[mask].reset_index(drop=True)

        final_rows = len(self.df)

        print(f"Linhas removidas por outliers: {initial_rows - final_rows}")
        print(f"Shape final: {self.df.shape}")