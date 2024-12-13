from typing import List


class CustomException(Exception):
    """Base class for all custom exceptions."""

    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class FileNotFoundErrorException(CustomException):
    """Raised when a file is not found."""

    def __init__(self, message="File not found", status_code=400):
        super().__init__(message, status_code)


class FileDeletionErrorException(CustomException):
    """Raised when there's an error deleting a file."""

    def __init__(self, message="Error deleting file", status_code=400):
        super().__init__(message, status_code)


class CSVParseErrorException(CustomException):
    """Raised when there's an error parsing the CSV."""

    def __init__(self, message="Error parsing CSV", status_code=400):
        super().__init__(message, status_code)


class DatabaseInsertErrorException(CustomException):
    """Raised when there's an error inserting data into the database."""

    def __init__(self, message="Error inserting data into database", status_code=400):
        super().__init__(message, status_code)


class QueryExecutionErrorException(CustomException):
    """Raised when there's an error executing the SQL query."""

    def __init__(self, message="Error executing query", status_code=400):
        super().__init__(message, status_code)


class InvalidColumnException(CustomException):
    """Raised when an invalid column is provided."""

    def __init__(self, column: str):
        message = f"Invalid column: {column}"
        super().__init__(message, status_code=422)


class InvalidOperationException(CustomException):
    """Raised when an invalid operation is used for a column."""

    def __init__(
        self,
        column: str,
        operation: str,
        allowed_operations: List[str],
        column_type: str,
    ):
        message = (
            f"Invalid operation '{operation}' for column '{column}' of type '{column_type}'. "
            f"Allowed operations: {', '.join(allowed_operations)}"
        )
        super().__init__(message, status_code=422)
