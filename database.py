import pymongo


class DataBase:
    client = None
    __db = None
    mongodb_version = None

    def __init__(self, configuration):
        self.configuration = configuration
        self.__connect(configuration['db_name'])

    def __connect(self, db_name: str):
        if self.configuration["uri"] not in ["", None]:
            try:
                self.client = pymongo.MongoClient(self.configuration["uri"])
                return
            except Exception as ex:
                print(f"Failed to connect to database using uri. >> {type(ex).__name__}")

        self.client = pymongo.MongoClient(
            host=self.configuration['host'],
            port=self.configuration['port'],
            username=self.configuration['username'],
            password=self.configuration['password'],
            authSource=self.configuration['authentication_source'],
        )
        try:
            self.mongodb_version = self.client.server_info()["version"]
            self.__db = self.client[db_name]
            print(f"Database <{self.configuration['alias']}> successfully connected.")

        except Exception as ex:
            print(f"Database <{self.configuration['alias']}> is not connected. >> {type(ex).__name__}")

    @property
    def get_db(self):
        return self.__db

    @property
    def name(self):
        return self.configuration['db_name']

    @property
    def alias(self):
        return self.configuration['alias']

    def get_collections_list(self):
        return self.__db.list_collection_names()

    def get_collection(self, collection_name):
        return self.__db[collection_name]

    def get_collection_documents(self, collection_name):
        return self.__db[collection_name].find()

    def get_collection_document(self, collection_name, document_id):
        return self.__db[collection_name].find_one({"_id": document_id})

    def store_documents_in_collection(self, collection_name, documents, delete_existing: bool = False) -> bool:
        collection = self.__db[collection_name]
        if delete_existing:
            self.delete_all_docs_in_collection(collection_name)
        for doc in documents:
            collection.insert_one(doc)
        return True

    def delete_doc_in_collection(self, collection_name, doc_id) -> bool:
        collection = self.__db[collection_name]
        collection.delete_many({"_id": doc_id})
        return True

    def delete_all_docs_in_collection(self, collection_name) -> bool:
        collection = self.__db[collection_name]
        collection.delete_many({})
        return True
