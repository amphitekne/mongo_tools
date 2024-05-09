import argparse

import manager
from config_reader import config_files
from database import DataBase


def get_db_config(alias: str) -> dict:
    for config_file_name in config_files:
        if config_files[config_file_name]["alias"] == alias:
            return config_files[config_file_name]


def main():
    # Initialize the parser
    parser = argparse.ArgumentParser(description="")

    # Adding arguments
    parser.add_argument('--source', type=str, help='Source mongo data base alias')
    parser.add_argument('--collection', type=str, help='Name of the collection to transfer')
    parser.add_argument('--field_name', type=str, help='')
    parser.add_argument('-r', '--remove', default=False, action=argparse.BooleanOptionalAction, help='')
    parser.add_argument('-b', '--backup', default=False, action=argparse.BooleanOptionalAction, help='')

    # Parse the arguments
    args = parser.parse_args()
    source = args.source
    collection = args.collection
    field_name = args.field_name
    remove = args.remove
    backup = args.backup


    source_db_config = get_db_config(source)
    source_db = DataBase(source_db_config)

    if remove:
        if backup:
            backup_db_config = source_db_config
            backup_db_config["db_name"] = backup_db_config["db_name"] + "_backup"
            backup_db = DataBase(backup_db_config)
            manager.remove_field_to_collection_with_backup(origin_db=source_db, origin_collection_name=collection,
                                                           field_name=field_name,
                                                           backup_db=backup_db, backup_collection_name=collection
                                                           )
        else:
            manager.remove_field_to_collection(origin_db=source_db, origin_collection_name=collection,
                                               field_name=field_name, )
    else:
        if backup:
            backup_db_config = source_db_config
            backup_db_config["db_name"] = backup_db_config["db_name"] + "_backup"
            backup_db = DataBase(backup_db_config)
            manager.add_new_field_to_collection_with_backup(origin_db=source_db, origin_collection_name=collection,
                                                            new_field_name=field_name, new_field_value=None,
                                                            backup_db=backup_db, backup_collection_name=collection
                                                            )
        else:
            manager.add_new_field_to_collection(origin_db=source_db, origin_collection_name=collection,
                                                new_field_name=field_name, new_field_value=None)

    print("Done.")


if __name__ == "__main__":
    main()
