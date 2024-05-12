from pymongo import MongoClient
import logging

class MongoHandler:
    def __init__(self, url):
        self.url = url
        self.client = MongoClient(self.url)
        self.db = None

    def connect(self, dbName):
        try:
            self.client = MongoClient(self.url)
            self.db = self.client[dbName]
            logging.info("Connected successfully to database")
        except Exception as e:
            logging.error(f"Connection to MongoDB failed: {e}")

    def disconnect(self):
        try:
            self.client.close()
            logging.info("Disconnected from database")
        except Exception as e:
            logging.error(f"Failed to disconnect from MongoDB: {e}")

    def create_document(self, collectionName, document):
        try:
            collection = self.db[collectionName]
            result = collection.insert_one(document)
            logging.info(f"A document was inserted with the _id: {result.inserted_id}")
            return result
        except Exception as e:
            logging.error(f"Create document failed: {e}")

    def read_documents(self, collectionName, query={}):
        try:
            collection = self.db[collectionName]
            documents = list(collection.find(query))
            return documents
        except Exception as e:
            logging.error(f"Read documents failed: {e}")

    def update_documents(self, collectionName, filter, updateDoc):
        try:
            collection = self.db[collectionName]
            result = collection.update_many(filter, {'$set': updateDoc})
            logging.info(f"{result.matched_count} document(s) matched the filter, updated {result.modified_count} document(s)")
            return result
        except Exception as e:
            logging.error(f"Update documents failed: {e}")

    def delete_documents(self, collectionName, query):
        try:
            collection = self.db[collectionName]
            result = collection.delete_many(query)
            logging.info(f"Deleted {result.deleted_count} documents")
            return result
        except Exception as e:
            logging.error(f"Delete documents failed: {e}")


    def document_exists(self, collectionName, itemId):
        """Check if a document with the given ID exists in the specified collection."""
        collection = self.db[collectionName]
        count = collection.count_documents({'_id': itemId})
        return count > 0

