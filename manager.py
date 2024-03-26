from database import DataBase


def transfer_individual_docs(origin_db: DataBase, origin_collection_name: str, origin_documents_ids: list[str] | str,
                             target_db: DataBase, target_collection_name: str) -> bool:
    if type(origin_documents_ids) == str:
        origin_documents_ids = [origin_documents_ids]

    origin_documents = []
    for document_id in origin_documents_ids:
        origin_documents.append(origin_db.get_collection_document(collection_name=origin_collection_name,
                                                                  document_id=document_id))

    target_db.store_documents_in_collection(collection_name=target_collection_name, documents=origin_documents)
    return True


def copy_index(origin_db: DataBase, origin_collection_name: str,
               target_db: DataBase, target_collection_name: str):
    indexes_to_copy = [index for index in origin_db.get_collection(origin_collection_name).list_indexes() if
                       index['name'] != '_id_']
    # Copy each index to the target collection
    for index in indexes_to_copy:
        # Extract index fields and options
        index_fields = index['key'].items()
        options = {k: v for k, v in index.items() if k not in ['v', 'key', 'ns']}
        # Create the index in the target collection
        target_db.get_collection(target_collection_name).create_index(list(index_fields), **options)


def transfer_complete_collection(origin_db: DataBase, origin_collection_name: str,
                                 target_db: DataBase, target_collection_name: str,
                                 delete_previous_docs: bool = False,
                                 include_index: bool = False) -> bool:
    origin_collection_documents = origin_db.get_collection_documents(origin_collection_name)
    if include_index:
        db = target_db.get_db
        temp_id = db[target_collection_name].insert_one({}).inserted_id
        db[target_collection_name].delete_one({'_id': temp_id})
        db[target_collection_name].find_one({"_id": temp_id})
        copy_index(origin_db, origin_collection_name,
                   target_db, target_collection_name)
    target_db.store_documents_in_collection(collection_name=target_collection_name,
                                            documents=origin_collection_documents,
                                            delete_existing=delete_previous_docs)
    return True


def transfer_complete_collection_with_backup(origin_db: DataBase, origin_collection_name: str,
                                             target_db: DataBase, target_collection_name: str,
                                             backup_db: DataBase,
                                             delete_previous_docs: bool = False) -> bool:
    # backup
    transfer_complete_collection(origin_db=origin_db, origin_collection_name=origin_collection_name,
                                 target_db=backup_db, target_collection_name=target_collection_name,
                                 delete_previous_docs=True)
    print(f'backup done on {backup_db.name}, collection: {target_collection_name}')
    # transfer
    origin_collection_documents = origin_db.get_collection_documents(origin_collection_name)
    target_db.store_documents_in_collection(collection_name=target_collection_name,
                                            documents=origin_collection_documents,
                                            delete_existing=delete_previous_docs)
    print(
        f'Transfer complete from <{origin_db.name}> collection <{origin_collection_name}> '
        f'to <{target_db.name}> collection <{target_collection_name}>')

    return True


def delete_collection_with_backup(origin_db: DataBase, origin_collection_name: str,
                                  backup_db: DataBase) -> bool:
    # backup
    transfer_complete_collection(origin_db=origin_db, origin_collection_name=origin_collection_name,
                                 target_db=backup_db, target_collection_name=origin_collection_name,
                                 delete_previous_docs=True)
    print(f'backup done on {backup_db.name}, collection: {origin_collection_name}')
    # deletion
    origin_db.delete_all_docs_in_collection(origin_collection_name)
    print(f'Deletion done.')


def add_new_field_to_complete_collection(db: DataBase, collection_name: str,
                                         new_field_name: str, new_field_value: any) -> bool:
    collection = db.get_collection(collection_name)
    collection.update_many({}, {"$set": {new_field_name: new_field_value}})
    return True


def add_new_field_to_complete_collection_with_backup(origin_db: DataBase, origin_collection_name: str,
                                                     new_field_name: str, new_field_value: any,
                                                     backup_db: DataBase
                                                     ) -> bool:
    # backup
    transfer_complete_collection(origin_db=origin_db, origin_collection_name=origin_collection_name,
                                 target_db=backup_db, target_collection_name=origin_collection_name,
                                 delete_previous_docs=True)
    print(f'backup done on {backup_db.name}, collection: {origin_collection_name}')
    collection = origin_db.get_collection(origin_collection_name)
    collection.update_many({}, {"$set": {new_field_name: new_field_value}})
    return True
