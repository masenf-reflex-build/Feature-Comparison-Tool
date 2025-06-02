import functools
import os
from contextlib import contextmanager
from typing import TYPE_CHECKING, Iterator
import databricks.sql
import pandas as pd
import reflex as rx
from databricks.sdk import WorkspaceClient
from databricks.sdk.core import Config
from databricks.sdk.service.files import DirectoryEntry

if TYPE_CHECKING:
    from databricks.sql.client import Cursor
    from databricks.sql.parameters.native import (
        TParameterCollection,
    )
databricks_cfg = Config()
databricks_http_path = (
    f"/sql/1.0/warehouses/{databricks_cfg.warehouse_id}"
)


def credentials_provider():
    return databricks_cfg.authenticate


@contextmanager
def databricks_cursor() -> Iterator["Cursor"]:
    with databricks.sql.connect(
        server_hostname=databricks_cfg.host,
        http_path=databricks_http_path,
        catalog=os.environ.get("DATABRICKS_CATALOG"),
        schema=os.environ.get("DATABRICKS_SCHEMA"),
        credentials_provider=credentials_provider,
    ) as connection, connection.cursor() as cursor:
        yield cursor


def sync_query_df(
    query: str,
    parameters: "TParameterCollection | None" = None,
) -> pd.DataFrame:
    with databricks_cursor() as cursor:
        cursor.execute(query, parameters=parameters)
        return cursor.fetchall_arrow().to_pandas()


async def async_query_df(
    query: str,
    parameters: "TParameterCollection | None" = None,
) -> pd.DataFrame:
    return await rx.run_in_thread(
        functools.partial(sync_query_df, query, parameters)
    )


def _get_full_path_for_volume_item(item_path: str) -> str:
    """
    Constructs the full path for an item in Databricks Volumes.
    If item_path is absolute (starts with '/'), it's returned as is.
    Otherwise, it's treated as relative to /Volumes/[catalog]/[schema]/.
    """
    if item_path.startswith("/"):
        return item_path
    current_prefix = "/Volumes"
    if catalog_env := os.environ.get("DATABRICKS_CATALOG"):
        current_prefix = (
            f"{current_prefix}/{catalog_env.strip('/')}"
        )
    if schema_env := os.environ.get("DATABRICKS_SCHEMA"):
        current_prefix = (
            f"{current_prefix}/{schema_env.strip('/')}"
        )
    if not current_prefix.endswith("/"):
        current_prefix += "/"
    clean_item_path = item_path.lstrip("/")
    return f"{current_prefix}{clean_item_path}"


def sync_list_directory(
    dir_path: str,
) -> list[DirectoryEntry]:
    w = WorkspaceClient(config=databricks_cfg)
    return w.files.list_directory(
        _get_full_path_for_volume_item(dir_path)
    )


async def async_list_directory(
    dir_path: str,
) -> list[DirectoryEntry]:
    return await rx.run_in_thread(
        functools.partial(sync_list_directory, dir_path)
    )


def sync_download_bytes(file_path: str) -> bytes:
    w = WorkspaceClient(config=databricks_cfg)
    return w.files.download(
        _get_full_path_for_volume_item(file_path)
    ).contents.read()


async def async_download_bytes(file_path: str) -> bytes:
    return await rx.run_in_thread(
        functools.partial(sync_download_bytes, file_path)
    )