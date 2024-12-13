import clickhouse_connect
from clickhouse_connect.driver.tools import insert_file
from app.constants import DB_NAME, DB_TABLES
from app.schema import GAME_ANALYTICS_COLUMNS
from app.utils import get_date_str
from decouple import config
from app.exceptions import DatabaseInsertErrorException
import os

# Define the environment configuration
ENVIRONMENT = os.environ.get("ENVIRONMENT") or "local"


# Configure the Clickhouse client based on the environment
def get_client():
    """
    Returns a Clickhouse client based on the environment configuration.

    If the environment is set to 'local', it connects to the Clickhouse instance running on localhost.
    Otherwise, it connects to the remote Clickhouse server using credentials from the environment.

    Returns:
        client (clickhouse_connect.client): The Clickhouse client instance.
    """
    if ENVIRONMENT == "local":
        return clickhouse_connect.get_client(
            host=config("DB_HOST"),
            user=("DB_USER"),
        )  # Localhost config
    else:
        return clickhouse_connect.get_client(
            host=os.environ.get("DB_HOST"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            secure=True,
        )


client = get_client()


def init_db():
    """
    Initializes the database by creating the database and tables if they do not already exist.

    Creates the necessary tables (`USERS`, `GAME_ANALYTICS`) and adds indexes to the `GAME_ANALYTICS` table.

    Returns:
        None
    """
    client.command(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    # Create Tables
    create_table(
        table_name=DB_TABLES.GAME_ANALYTICS,
        columns=GAME_ANALYTICS_COLUMNS,
        order_by="appid",
    )
    client.command(
        f"ALTER TABLE {str(DB_TABLES.GAME_ANALYTICS)} ADD INDEX IF NOT EXISTS idx_age (required_age) TYPE minmax GRANULARITY 4"
    )
    client.command(
        f"ALTER TABLE {str(DB_TABLES.GAME_ANALYTICS)} ADD INDEX IF NOT EXISTS idx_release_date (release_date) TYPE minmax GRANULARITY 4"
    )
    client.command(
        f"ALTER TABLE {str(DB_TABLES.GAME_ANALYTICS)} ADD INDEX IF NOT EXISTS idx_name (name) TYPE bloom_filter(0.01) GRANULARITY 4"
    )


def create_table(
    table_name: str,
    columns: list,
    order_by: str = None,
    engine: str = "MergeTree",
):
    """
    Creates a table in the database with the specified columns and options.

    Args:
        table_name (str): The name of the table to be created.
        columns (list): A list of column definitions as strings (e.g., "column_name DataType").
        order_by (str, optional): The column to order the table by (default is None).
        engine (str, optional): The table engine to use (default is 'MergeTree').

    Returns:
        None
    """
    columns_definition = ", ".join(columns)

    # Build the CREATE TABLE query
    query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} ({columns_definition}) ENGINE = {engine}
    """
    if order_by:
        query += f" ORDER BY {order_by}"

    try:
        # Execute the query
        client.command(query)
        print(f"Table '{table_name}' created or already exists.")
    except Exception as e:
        print(f"Failed to create '{table_name}' table. Error: {e}")


def insert_from_csv(table_name: str, csv_path: str):
    """
    Inserts data into the specified table from a given CSV file.

    Args:
        table_name (str): Table name where the data will be inserted.
        csv_path (str): File path of the CSV to be inserted.

    Returns:
        None
    """
    try:
        insert_file(client, str(table_name), csv_path)
        print(
            f"Successfully inserted data from '{csv_path}' into the table '{table_name}'."
        )
    except Exception as e:
        raise DatabaseInsertErrorException(
            message="Failed to insert data from '{csv_path}' into the table '{table_name}'. Error: {e}"
        )


def fetch_rows_by_query(query: str):
    """
    Executes a query on the database and fetches the results, converting them to a list of dictionaries.

    Args:
        query (str): The SQL query to be executed.

    Returns:
        rows (list): A list of dictionaries where each dictionary represents a row, with keys as column names.
    """
    results = client.query(query)

    # Convert results to a list of dictionaries
    column_names = results.column_names
    rows = []
    for row in results.result_rows:
        row_dict = dict(zip(column_names, row))
        row_dict["release_date"] = get_date_str(row_dict["release_date"])
        row_dict["created_at"] = get_date_str(row_dict["created_at"])
        row_dict["price"] = "{0:.2f}".format(row_dict["price"])
        rows.append(row_dict)
    return rows


def insert_row(table_name, row):
    """
    Inserts a single row of data into the specified table.

    Args:
        table_name (str): Table name where the row will be inserted.
        row (dict): A dictionary containing column names as keys and the respective values for the row.

    Returns:
        result: The result of the insert operation.
    """
    columns = list(row.keys())
    values = list(row.values())

    result = client.insert(table=table_name, column_names=columns, data=[values])

    return result


def fetch_row(table_name, columns="*", conditions={}):
    """
    Fetches a single row from a table based on the given conditions.

    Args:
        table_name (str): The name of the table to fetch data from.
        columns (str, optional): The columns to fetch. Defaults to "*" (all columns).
        conditions (dict, optional): A dictionary of conditions to filter the results by.

    Returns:
        dict: A dictionary representing the fetched row with column names as keys and values.
    """
    where_clause = " AND ".join(f"{k} = '{v}'" for k, v in conditions.items())
    query = "SELECT {columns} FROM {table} WHERE {where_clause}".format(
        columns=columns, table=table_name, where_clause=where_clause
    )
    result = client.query(query=query)
    rows = []
    for row in result.result_rows:
        row_dict = dict(zip(result.column_names, row))
        rows.append(row_dict)
    return rows[0]
