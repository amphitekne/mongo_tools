import argparse

import manager
from config_reader import config_files
from database import DataBase


def connect(source: str, target: str) -> dict:
    data_bases = {}
    for config_file_name in config_files:
        if config_files[config_file_name]["alias"] in [source, target]:
            data_bases[config_files[config_file_name]["alias"]] = DataBase(config_files[config_file_name])
    return data_bases


def main():
    # Initialize the parser
    parser = argparse.ArgumentParser(description='')

    # Adding arguments
    parser.add_argument('--source', type=str, help='Source mongo data base alias')
    parser.add_argument('--target', type=str, help='Target mongo data base alias')

    # Parse the arguments
    args = parser.parse_args()
    source = args.source
    target = args.target

    print("Connecting to databases...")
    data_bases = connect(source, target)
    collections = data_bases[source].get_collections_list()
    for collection in collections:
        print(f"Copying {collection} collection...")
        manager.transfer_complete_collection(origin_db=data_bases[source], origin_collection_name=collection,
                                             target_db=data_bases[target], target_collection_name=collection,
                                             delete_previous_docs=True)
    print("Done.")


if __name__ == "__main__":
    main()
