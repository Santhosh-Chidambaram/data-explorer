GAME_ANALYTICS_SCHEMA = {
    "id": "VARCHAR(69) DEFAULT generateUUIDv4()",
    "appid": "UInt32",
    "name": "String",
    "release_date": "Nullable(Date)",
    "required_age": "UInt32",
    "price": "Float32",
    "dlc_count": "UInt32",
    "about_the_game": "String",
    "supported_languages": "Array(String)",
    "windows": "Bool",
    "mac": "Bool",
    "linux": "Bool",
    "positive": "UInt32",
    "negative": "UInt32",
    "score_rank": "UInt32",
    "developers": "String",
    "publishers": "String",
    "categories": "String",
    "genres": "String",
    "tags": "String",
    "created_at": "DateTime DEFAULT now()",
}

GAME_ANALYTICS_COLUMNS = [
    f"{column} {data_type}" for column, data_type in GAME_ANALYTICS_SCHEMA.items()
]
