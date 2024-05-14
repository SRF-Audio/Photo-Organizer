from modules.jxaHandler import execute_jxa_script
from modules.mongoHandler import MongoHandler
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def retrieveAndStoreMetadata(mediaItems, mongo, mongoCollection):
    """Store or update metadata for media items in the MongoDB collection."""
    new_items_added = 0
    updates_made = 0
    for item in mediaItems:
        item_id = item['_id']
        if not mongo.document_exists(mongoCollection, item_id):
            mongo.create_document(mongoCollection, item)
            new_items_added += 1
        else:
            existing_item = mongo.read_documents(mongoCollection, {'_id': item_id})[0]
            updated_fields = {}
            
            for key, value in item.items():
                if key != '_id' and existing_item.get(key) != value:
                    if key == 'keywords':
                        existing_keywords = set(existing_item.get('keywords', []))
                        new_keywords = set(value)
                        combined_keywords = list(existing_keywords.union(new_keywords))
                        if existing_keywords != combined_keywords:
                            updated_fields['keywords'] = combined_keywords
                    else:
                        updated_fields[key] = value
            
            if updated_fields:
                mongo.update_documents(mongoCollection, {'_id': item_id}, updated_fields)
                updates_made += 1

    logging.info(f"Added {new_items_added} new media items to the collection.")
    logging.info(f"Updated metadata for {updates_made} items in the collection.")

def main():
    db_url = "mongodb://localhost:27017"
    db_name = "photoOrganizer"
    collection_name = "mediaItemMetadata"

    mongo_handler = MongoHandler(db_url)
    mongo_handler.connect(db_name)

    logging.info("Executing JXA script to retrieve media items metadata.")
    retrieve_mediaItem_path = "./jxa-scripts/retrieveMediaItemMetadata.js"
    result = execute_jxa_script(retrieve_mediaItem_path)
    if result:
        logging.info("Media items metadata retrieved successfully.")
        if 'mediaItems' in result:
            retrieveAndStoreMetadata(result['mediaItems'], mongo_handler, collection_name)
        else:
            logging.info("No media items to process.")
    else:
        logging.error("Failed to retrieve media items metadata.")

    mongo_handler.disconnect()

if __name__ == "__main__":
    main()
