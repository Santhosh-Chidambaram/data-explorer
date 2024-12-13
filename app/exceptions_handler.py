from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.exceptions import (
    FileNotFoundErrorException,
    FileDeletionErrorException,
    CSVParseErrorException,
    DatabaseInsertErrorException,
    QueryExecutionErrorException,
    InvalidOperationException,
    InvalidColumnException,
)


def register_exception_handlers(app: FastAPI):
    """Register global exception handlers."""

    @app.exception_handler(FileNotFoundErrorException)
    async def file_not_found_exception_handler(
        request, exc: FileNotFoundErrorException
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={"status": exc.status_code, "message": exc.message},
        )

    @app.exception_handler(FileDeletionErrorException)
    async def file_deletion_exception_handler(request, exc: FileDeletionErrorException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"status": exc.status_code, "message": exc.message},
        )

    @app.exception_handler(CSVParseErrorException)
    async def csv_parse_exception_handler(request, exc: CSVParseErrorException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"status": exc.status_code, "message": exc.message},
        )

    @app.exception_handler(DatabaseInsertErrorException)
    async def database_insert_exception_handler(
        request, exc: DatabaseInsertErrorException
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={"status": exc.status_code, "message": exc.message},
        )

    @app.exception_handler(QueryExecutionErrorException)
    async def query_execution_exception_handler(
        request, exc: QueryExecutionErrorException
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={"status": exc.status_code, "message": exc.message},
        )

    @app.exception_handler(InvalidColumnException)
    async def invalid_column_exception_handler(
        request, exc: QueryExecutionErrorException
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={"status": exc.status_code, "message": exc.message},
        )

    @app.exception_handler(InvalidOperationException)
    async def invalid_operation_exception_handler(
        request, exc: QueryExecutionErrorException
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={"status": exc.status_code, "message": exc.message},
        )

    # Generic 500 error handler for all other unhandled exceptions
    @app.exception_handler(Exception)
    async def generic_exception_handler(request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"message": f"An unexpected error occurred: {str(exc)}"},
        )
