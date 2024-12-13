import os
import random
import string
from datetime import datetime
from io import StringIO

import pandas as pd
import requests
from app.exceptions import (
    CSVParseErrorException,
    FileDeletionErrorException,
    FileNotFoundErrorException,
)

# Utility Functions


def delete_file(file_path: str) -> bool:
    """
    Deletes a file from the given file path.

    Args:
        file_path (str): Path to the file to be deleted.

    Returns:
        bool: True if the file is successfully deleted.

    Raises:
        FileNotFoundErrorException: If the file does not exist.
        FileDeletionErrorException: If an error occurs during deletion.
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File '{file_path}' has been deleted.")
            return True
        else:
            raise FileNotFoundErrorException(message=f"File '{file_path}' not found.")
    except Exception as e:
        raise FileDeletionErrorException(
            message=f"Error occurred while deleting the file in {file_path}: {e}"
        )


def format_date_str(date_str: str) -> str:
    """
    Formats a date string from 'Month Day, Year' to 'YYYY-MM-DD'.

    Args:
        date_str (str): Date string in the format 'Month Day, Year'.

    Returns:
        str: Formatted date string in 'YYYY-MM-DD'. Returns None if formatting fails.
    """
    try:
        return datetime.strptime(date_str, "%b %d, %Y").strftime("%Y-%m-%d")
    except ValueError:
        return None


def get_date_str(date_instance: datetime) -> str:
    """
    Converts a datetime instance to a string in 'YYYY-MM-DD' format.

    Args:
        date_instance (datetime): Datetime object to be converted.

    Returns:
        str: Date string in 'YYYY-MM-DD' format, or None if the input is invalid.
    """
    return date_instance.strftime("%Y-%m-%d") if date_instance else None


def get_random_str() -> str:
    """
    Generates a random string of 8 alphanumeric characters.

    Returns:
        str: Random string.
    """
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=8))


def to_snake_case(col_str: str) -> str:
    """
    Converts a string to snake_case.

    Args:
        col_str (str): String to be converted.

    Returns:
        str: String in snake_case.
    """
    return col_str.strip().lower().replace(" ", "_")


# Core Functionality


def parse_and_download_csv(csv_url: str) -> str:
    """
    Downloads a CSV file from the given URL, processes it, and saves it locally.

    Args:
        csv_url (str): URL of the CSV file to download.

    Returns:
        str: File path of the processed and saved CSV file.

    Raises:
        CSVParseErrorException: If an error occurs during downloading or processing.
    """
    try:
        # Download CSV data from the URL
        response = requests.get(csv_url)
        response.raise_for_status()
        csv_data = response.content.decode("utf-8")

        # Parse CSV into a DataFrame
        df = pd.read_csv(StringIO(csv_data))

        # Remove the first column (assuming it's an index-like column)
        df = df.loc[:, df.columns != df.columns[0]]

        # Convert column names to snake_case
        df.columns = [to_snake_case(col) for col in df.columns]

        # Format release_date column
        if "release_date" in df.columns:
            df["release_date"] = df["release_date"].apply(format_date_str)

        # Generate output file name
        output_csv = f"analytics_{get_random_str()}.csv"

        # Save processed DataFrame to a new CSV file
        df.to_csv(output_csv, index=False)

        return output_csv
    except requests.exceptions.RequestException as e:
        raise CSVParseErrorException(
            message=f"Failed to download CSV. Please check the URL: {e}"
        )
