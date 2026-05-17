"""Configuration module for the diabetes model template.

This module defines structured configuration objects used to load project
settings from a YAML file and to standardize MLflow tracking tags.
"""

from typing import Any

import yaml
from pydantic import BaseModel


class ProjectConfig(BaseModel):
    """Represent project configuration parameters loaded from a YAML file.

    This model centralizes the main configuration required by the diabetes
    modeling pipeline, including numerical features, categorical features,
    target variable, Unity Catalog location, model parameters, and MLflow
    experiment names.

    The configuration supports multiple execution environments, such as
    development, staging, and production. Environment-specific values are
    selected when the configuration is loaded from YAML.
    """

    num_features: list[str]
    cat_features: list[str]
    target: str
    catalog_name: str
    schema_name: str
    parameters: dict[str, Any]
    experiment_name_basic: str | None
    experiment_name_custom: str | None

    @classmethod
    def from_yaml(cls, config_path: str, env: str = "dev") -> "ProjectConfig":
        """Load project configuration from a YAML file.

        The YAML file is expected to contain general project settings and
        environment-specific sections for ``dev``, ``stg``, and ``prd``.
        Based on the selected environment, this method extracts the correct
        catalog and schema names and returns a validated ``ProjectConfig``
        instance.

        :param config_path: Path to the YAML configuration file.
        :param env: Execution environment to load. Accepted values are
            ``dev``, ``stg``, and ``prd``. Defaults to ``dev``.
        :return: Validated ``ProjectConfig`` instance populated with the
            selected environment settings.
        :raises ValueError: If the provided environment is not one of
            ``dev``, ``stg``, or ``prd``.
        """
        if env not in ["prd", "stg", "dev"]:
            raise ValueError(f"Invalid environment: {env}. Expected 'prd', 'stg', or 'dev'")

        with open(config_path) as f:
            config_dict = yaml.safe_load(f)
            config_dict["catalog_name"] = config_dict[env]["catalog_name"]
            config_dict["schema_name"] = config_dict[env]["schema_name"]

            return cls(**config_dict)


class Tags(BaseModel):
    """Represent metadata tags used for MLflow experiment tracking.

    These tags help improve experiment traceability by linking each MLflow
    run to the Git commit, branch, and optionally another related MLflow
    run identifier.
    """

    git_sha: str
    branch: str
    run_id: str | None = None

    def to_dict(self) -> dict[str, str | None]:
        """Convert the MLflow tags model into a dictionary.

        The returned dictionary can be passed directly to MLflow tag-setting
        functions. The optional ``run_id`` field is included only when it is
        available, avoiding unnecessary tags with null values.

        :return: Dictionary containing Git and run metadata for MLflow.
        """
        tags_dict = {}
        tags_dict["git_sha"] = self.git_sha
        tags_dict["branch"] = self.branch
        if self.run_id is not None:
            tags_dict["run_id"] = self.run_id
        return tags_dict