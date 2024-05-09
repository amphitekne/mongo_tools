import manager
from config_reader import get_configuration
from database import DataBase

source_db_config = get_configuration(alias="db_alias")
source_db = DataBase(source_db_config)


print("Removing fields:")
fields_to_remove = [("collection_name", "field_name"), ("collection_name", "field_name")]

for collection, field_name in fields_to_remove:
    print(f"Collection: {collection}. Field: {field_name}")
    manager.remove_field_to_collection(
        origin_db=source_db,
        origin_collection_name=collection,
        field_name=field_name,
    )
print("Removing task Done.")

print()

print("Adding new field(s) to collection(s):")
# ("collection_name", "field_name", "value")
fields_to_add = [
    ("collection_name", "field_name", "hello"),
    ("collection_name", "field_name", None),
    ("collection_name", "field_name", 74.0),
    (
        "collection_name",
        "field_name",
        {
            "xx": 0,
            "yy": 0,
            "zz": 0,
            "ss": 0,
        },
    ),
    ("collection_name", "field_name", True),
]

for collection, field_name, field_value in fields_to_add:
    manager.add_new_field_to_collection(
        origin_db=source_db,
        origin_collection_name=collection,
        new_field_name=field_name,
        new_field_value=field_value,
    )
