from modules.jxaHandler import execute_jxa_script
from modules.mongoHandler import MongoHandler
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def newMediaItemFilter(mediaItemIds, mongo, mongoCollection):
    """Filter and add new media items to the MongoDB collection if they don't already exist."""
    new_items_added = 0
    for item_id in mediaItemIds:
        if not mongo.document_exists(mongoCollection, item_id):
            document = {'_id': item_id}
            mongo.create_document(mongoCollection, document)
            new_items_added += 1
    logging.info(f"Added {new_items_added} new media items to the collection.")

def main():
    db_url = "mongodb://localhost:27017"
    db_name = "photoOrganizer"
    collection_name = "mediaItemIds"

    mongo_handler = MongoHandler(db_url)
    mongo_handler.connect(db_name)

    retrieve_mediaItem_path = "./jxa-scripts/retrieveMediaItemIds.js"
    result = execute_jxa_script(retrieve_mediaItem_path)

    if result:
        logging.info("Script executed successfully:")
        media_item_ids = result.get('mediaItems', [])
        if media_item_ids:
            newMediaItemFilter(media_item_ids, mongo_handler, collection_name)
        else:
            logging.info("No new media items to process.")
    else:
        logging.error("Script execution failed.")

    mongo_handler.disconnect()

if __name__ == "__main__":
    main()
