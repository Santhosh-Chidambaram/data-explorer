# api.py
from fastapi import APIRouter
from pydantic import BaseModel, HttpUrl
from fastapi.responses import JSONResponse
from app.utils import parse_and_download_csv, delete_file
from app.db import insert_from_csv, fetch_rows_by_query
from app.constants import DB_TABLES, OPERATION_MAPPING, ALLOWED_OPERATIONS
from app.schema import GAME_ANALYTICS_SCHEMA
from app.exceptions import InvalidColumnException, InvalidOperationException
from pydantic import BaseModel
from typing import List, Literal, Optional

router = APIRouter(
    prefix="/data-explorer",
    tags=["data-explorer"],
)


class CsvUploadRequest(BaseModel):
    csv_url: HttpUrl


# Define the schema for a single filter
class FilterParam(BaseModel):
    column: str
    value: str
    operation: Literal["eq", "like", "lt", "gt", "lte", "gte"]


# Define the schema for the query request
class QueryRequest(BaseModel):
    filters: Optional[List[FilterParam]] = []


@router.post("/upload-csv")
async def upload_csv(request: CsvUploadRequest):
    csv_url = request.csv_url
    csv_file_path = parse_and_download_csv(csv_url)
    insert_from_csv(DB_TABLES.GAME_ANALYTICS, csv_file_path)
    delete_file(csv_file_path)
    return JSONResponse(
        content={
            "status": 200,
            "message": "CSV uploaded and processed successfully.",
            "data": {},
        }
    )


def build_query(params: any) -> str:
    query_parts = []
    for param in params:
        column = param.column
        value = param.value
        sql_operator = OPERATION_MAPPING[param.operation]
        column_type = GAME_ANALYTICS_SCHEMA[column]
        if column_type == "String":
            if sql_operator == "LIKE":
                value = f"'%{value}%'"
            else:
                value = f"'{value}'"
        elif column_type in ["Nullable(Date)", "DateTime DEFAULT now()"]:
            value = f"'{value}'"
        query_parts.append(f"{column} {sql_operator} {value}")
    return " AND ".join(query_parts)


def validate_filters(filters: List[dict]) -> None:
    """
    Validates the filters for the /query endpoint.

    Args:
        filters (List[dict]): List of filters to validate.

    Raises:
        InvalidColumnException: If a column is invalid.
        InvalidOperationException: If an operation is invalid for the column type.
    """
    for filter_param in filters:
        column = filter_param.column
        operation = filter_param.operation

        # Check if the column is valid
        if column not in GAME_ANALYTICS_SCHEMA:
            raise InvalidColumnException(column)

        # Get the data type of the column from the schema
        column_type = GAME_ANALYTICS_SCHEMA[column].split()[0]

        # Check if the operation is valid for the column's data type
        allowed_operations = ALLOWED_OPERATIONS.get(column_type)
        if not allowed_operations or operation not in allowed_operations:
            raise InvalidOperationException(
                column, operation, allowed_operations, column_type
            )


@router.post("/query")
async def data_explorer(request: QueryRequest):
    # Validate filters
    validate_filters(request.filters)

    where_clause = ""
    if len(request.filters) > 0:
        where_clause = build_query(request.filters)
    query = f"SELECT * FROM {DB_TABLES.GAME_ANALYTICS}"
    if where_clause:
        query += f" WHERE {where_clause}"
    data = fetch_rows_by_query(query)
    return JSONResponse(
        content={
            "status": 200,
            "message": "Fetched data sucessfully!",
            "data": data,
        }
    )
