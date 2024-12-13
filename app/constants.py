from enum import Enum

# Database Name
DB_NAME = "data_explorer"


# Enum to represent the database tables
class DB_TABLES(Enum):
    GAME_ANALYTICS = f"{DB_NAME}.game_analytics"

    def __str__(self):
        return self.value


# Operation mappings for filtering queries
OPERATION_MAPPING = {
    "eq": "=",
    "lt": "<",
    "gt": ">",
    "lte": "<=",
    "gte": ">=",
    "ne": "!=",
    "like": "LIKE",
}

ALLOWED_OPERATIONS = {
    "String": ["eq", "like"],
    "Nullable(Date)": ["eq", "lt", "gt", "lte", "gte"],
    "UInt32": ["eq", "lt", "gt", "lte", "gte"],
    "Float32": ["eq", "lt", "gt", "lte", "gte"],
    "Bool": ["eq"],
}
