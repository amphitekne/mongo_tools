import socket

import pymongo
from sshtunnel import SSHTunnelForwarder


def get_port() -> int:
    def is_port_in_use(port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0

    tunnel_port = 27017
    while True:
        if not is_port_in_use(tunnel_port):
            return tunnel_port
        else:
            tunnel_port += 1


class DataBase:
    client = None
    __db = None
    mongodb_version = None
    server = None

    def __init__(self, configuration):
        self.configuration = configuration
        self.__connect(configuration["mongo"]['db_name'])

    def __connect(self, db_name: str):
        if self.configuration["uri"] not in ["", None, False]:
            try:
                self.client = pymongo.MongoClient(self.configuration["uri"])
                return
            except Exception as ex:
                raise ConnectionError(f"Failed to connect to database using uri. >> {type(ex).__name__}")

        elif self.configuration["host"]["ip"] not in ["localhost", "127.0.0.1"]:
            local_port = get_port()
            print(f"The local port is {local_port}")
            self.server = SSHTunnelForwarder(
                (self.configuration["host"]["ip"], 22),
                ssh_username=self.configuration["host"]["user_name"],
                ssh_password=self.configuration["host"]["password"],
                remote_bind_address=('127.0.0.1', 27017),
                local_bind_address=('127.0.0.1', local_port)
            )
            self.server.start()
        else:
            local_port = self.configuration["host"]["local_port"]

        self.client = pymongo.MongoClient(
            host="127.0.0.1",
            port=local_port,
            username=self.configuration['mongo']["username"],
            password=self.configuration['mongo']["password"],
            authSource=self.configuration['mongo']['authentication_source'],
        )
        try:
            self.mongodb_version = self.client.server_info()["version"]
            self.__db = self.client[db_name]
            print(f"Database <{self.configuration['alias']}> successfully connected.")

        except Exception as ex:
            print(f"Database <{self.configuration['alias']}> is not connected. >> {type(ex).__name__}")

    def close_server(self):
        self.server.stop()

    @property
    def get_db(self):
        return self.__db

    @property
    def name(self):
        return self.configuration["mongo"]['db_name']

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
