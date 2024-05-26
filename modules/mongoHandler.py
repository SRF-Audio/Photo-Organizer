from pymongo import MongoClient
import logging

class MongoHandler:
    def __init__(self, url, db_name):
        self.url = url
        self.db_name = db_name
        self.client = None
        self.db = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

    def connect(self):
        try:
            self.client = MongoClient(self.url)
            self.db = self.client[self.db_name]
            logging.info("Connected successfully to database")
        except Exception as e:
            logging.error(f"Connection to MongoDB failed: {e}")
            raise

    def disconnect(self):
        try:
            if self.client:
                self.client.close()
                logging.info("Disconnected from database")
        except Exception as e:
            logging.error(f"Failed to disconnect from MongoDB: {e}")

    def collection_exists(self, collection_name):
        try:
            logging.debug(f"Checking existence of collection: {collection_name}")
            collection_names = self.db.list_collection_names()
            exists = collection_name in collection_names
            logging.debug(f"Collection {collection_name} exists: {exists}")
            return exists
        except Exception as e:
            logging.error(f"Check collection existence failed: {e}")
            raise


    def create_document(self, collection_name, document):
        try:
            collection = self.db[collection_name]
            result = collection.insert_one(document)
            logging.info(f"A document was inserted with the _id: {result.inserted_id}")
            return result
        except Exception as e:
            logging.error(f"Create document failed: {e}")
            raise

    def read_documents(self, collection_name, query={}):
        try:
            logging.debug(f"Querying documents in {collection_name} with query: {query}")
            collection = self.db[collection_name]
            documents = list(collection.find(query))
            logging.debug(f"Retrieved {len(documents)} documents")
            return documents
        except Exception as e:
            logging.error(f"Read documents failed: {e}")
            raise

    def update_documents(self, collection_name, filter, update_doc):
        try:
            logging.debug(f"Updating documents in {collection_name} with filter: {filter} and update_doc: {update_doc}")
            collection = self.db[collection_name]
            result = collection.update_many(filter, {'$set': update_doc})
            logging.info(f"{result.matched_count} document(s) matched the filter, updated {result.modified_count} document(s)")
            return result
        except Exception as e:
            logging.error(f"Update documents failed: {e}")
            raise

    def delete_documents(self, collection_name, query):
        try:
            logging.debug(f"Deleting documents in {collection_name} with query: {query}")
            collection = self.db[collection_name]
            result = collection.delete_many(query)
            logging.info(f"Deleted {result.deleted_count} documents")
            return result
        except Exception as e:
            logging.error(f"Delete documents failed: {e}")
            raise

    def document_exists(self, collection_name, item_id):
        """Check if a document with the given ID exists in the specified collection."""
        try:
            logging.debug(f"Checking existence of document with _id: {item_id} in {collection_name}")
            collection = self.db[collection_name]
            count = collection.count_documents({'_id': item_id})
            logging.debug(f"Document with _id: {item_id} exists: {count > 0}")
            return count > 0
        except Exception as e:
            logging.error(f"Check document existence failed: {e}")
            raise

    def update_api_responses(self, media_item_id, aws_response, gpt_response):
        try:
            collection = self.db['apiResponses']
            document = {
                '_id': media_item_id,
                'aws_responses': aws_response,
                'gpt_response': gpt_response
            }
            collection.update_one({'_id': media_item_id}, {'$set': document}, upsert=True)
            logging.info(f"API responses for media item {_id} updated successfully.")
        except Exception as e:
            logging.error(f"Failed to update API responses: {e}")
            raise
