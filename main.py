from modules.jxaHandler import execute_jxa_script
from modules.mongoHandler import MongoHandler
import logging
import json

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
            existing_item = mongo.read_document(mongoCollection, item_id)
            if existing_item['metadata'] != item['metadata']:
                mongo.update_document(mongoCollection, item_id, {'metadata': item['metadata']})
                updates_made += 1

    logging.info(f"Added {new_items_added} new media items to the collection.")
    logging.info(f"Updated metadata for {updates_made} items in the collection.")

def main():
    db_url = "mongodb://localhost:27017"
    db_name = "photoOrganizer"
    collection_name = "mediaItemMetadata"

    mongo_handler = MongoHandler(db_url)
    mongo_handler.connect(db_name)

    retrieve_mediaItem_path = "./jxa-scripts/retrieveMediaItemMetadata.js"
    result = execute_jxa_script(retrieve_mediaItem_path)
    if result:
        logging.info("Media items metadata retrieved successfully.")
        mediaItems = json.loads(result) 
        if mediaItems.get('mediaItems'):
            retrieveAndStoreMetadata(mediaItems['mediaItems'], mongo_handler, collection_name)
        else:
            logging.info("No media items to process.")
    else:
        logging.error("Failed to retrieve media items metadata.")

    mongo_handler.disconnect()

if __name__ == "__main__":
    main()
