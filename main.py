import logging
import os
from dotenv import load_dotenv
from modules.jxaHandler import execute_jxa_script, handle_media_export, parse_script_output, delete_exported_file
from modules.mongoHandler import MongoHandler
from modules.awsHandler import AWSHandler
from modules.openAiHandler import OpenAIHandler

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def retrieve_and_store_metadata(media_items, mongo, mongo_collection):
    logging.debug(f"Starting retrieve_and_store_metadata with {len(media_items)} media items.")
    new_items_added = 0
    updates_made = 0
    for item in media_items:
        item_id = item['_id']
        if not mongo.document_exists(mongo_collection, item_id):
            mongo.create_document(mongo_collection, item)
            new_items_added += 1
        else:
            existing_item = mongo.read_documents(mongo_collection, {'_id': item_id})[0]
            updated_fields = get_updated_fields_from_photos(existing_item, item)
            if updated_fields:
                mongo.update_documents(mongo_collection, {'_id': item_id}, updated_fields)
                updates_made += 1
    logging.info(f"Added {new_items_added} new media items to the collection.")
    logging.info(f"Updated metadata for {updates_made} items in the collection.")

def get_updated_fields_from_photos(existing_item, new_item):
    updated_fields = {}
    for key, value in new_item.items():
        if key != '_id' and existing_item.get(key) != value:
            if key == 'keywords':
                existing_keywords = set(existing_item.get('keywords', []))
                new_keywords = set(value)
                combined_keywords = list(existing_keywords.union(new_keywords))
                if existing_keywords != combined_keywords:
                    updated_fields['keywords'] = combined_keywords
            else:
                updated_fields[key] = value
    logging.debug(f"Updated fields for item: {updated_fields}")
    return updated_fields

def handle_missing_metadata(mongo, mongo_collection, aws_handler, openai_handler):
    query = {
        "$or": [
            {"name": {"$exists": False}},
            {"name": None},
            {"description": {"$exists": False}},
            {"description": None},
            {"keywords": {"$exists": True, "$lt": 5}}
        ]
    }
    media_items = mongo.read_documents(mongo_collection, query)
    logging.info(f"Found {len(media_items)} media items with missing metadata.")
    for item in media_items:
        item_id = item['_id']
        logging.info(f"Processing media item with ID: {item_id}")
        if item.get('name') is None or item.get('name') == "":
            process_missing_name(item, openai_handler)
        if item.get('description') is None or item.get('description') == "":
            process_missing_description(item, openai_handler)
        if len(item.get('keywords', [])) < 5:
            process_missing_keywords(item, aws_handler)
        mongo.update_documents(mongo_collection, {'_id': item_id}, item)

def process_missing_name(item, openai_handler):
    logging.info(f"Missing name for item ID: {item['_id']}. Generating name using OpenAI.")
    prompt = f"Generate a title for a photo with these keywords: {', '.join(item.get('keywords', []))}"
    item['name'] = openai_handler.enhance_descriptions(item['_id'], prompt)

def process_missing_description(item, openai_handler):
    logging.info(f"Missing description for item ID: {item['_id']}. Generating description using OpenAI.")
    prompt = f"Generate a description for a photo with these keywords: {', '.join(item.get('keywords', []))}"
    item['description'] = openai_handler.enhance_descriptions(item['_id'], prompt)

def process_missing_keywords(item, aws_handler):
    logging.info(f"Missing keywords for item ID: {item['_id']}. Generating keywords using AWS Rekognition.")
    export_path = handle_media_export(item['_id'])
    if export_path:
        keywords = aws_handler.detect_labels(export_path)
        item['keywords'] = list(set(item.get('keywords', [])).union(set(keywords)))
    else:
        logging.error(f"Failed to export media item with ID: {item['_id']}")

def process_media_item(mongo, mongo_collection, item, aws_handler, openai_handler):
    item_id = item['_id']
    export_path = handle_media_export(item_id)
    if export_path:
        logging.info(f"Media item exported successfully to {export_path}.")
        
        # AWS Rekognition - Detect labels and faces
        labels = aws_handler.detect_labels(export_path)
        face_details = aws_handler.detect_faces(export_path)
        face_ids = aws_handler.index_faces(export_path)
        
        # Prepare data for OpenAI
        existing_keywords = set(item.get('keywords', []))
        combined_keywords = list(existing_keywords.union(labels))
        face_descriptions = [f"FaceId: {face['FaceId']}, BoundingBox: {face['BoundingBox']}" for face in face_details]
        face_descriptions_str = ' '.join(face_descriptions)
        
        # OpenAI for enhanced description
        enhanced_description = openai_handler.enhance_descriptions(export_path, combined_keywords)

        update_doc = {
            'keywords': combined_keywords,
            'description': enhanced_description,
            'faces': face_ids
        }
        mongo.update_documents(mongo_collection, {'_id': item_id}, update_doc)
        logging.info(f"Updated metadata for media item {item_id}.")

        # Store API responses
        aws_responses = {
            'labels': labels,
            'faces': face_details,
            'indexed_faces': face_ids
        }
        mongo.update_api_responses(item_id, aws_responses, enhanced_description)
        
        # Delete the exported file
        delete_exported_file(export_path)
    else:
        logging.error(f"Failed to export media item with ID: {item_id}")

def main():
    db_url = os.getenv('MONGO_URL')
    db_name = os.getenv('DB_NAME')
    collection_name = os.getenv('COLLECTION_NAME')
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    region_name = os.getenv('AWS_REGION')
    openai_api_key = os.getenv('OPENAI_API_KEY')
    rekognition_collection_id = os.getenv('REKOGNITION_COLLECTION_ID')

    aws_handler = AWSHandler(aws_access_key_id, aws_secret_access_key, region_name, rekognition_collection_id)
    openai_handler = OpenAIHandler(openai_api_key)

    # Create Rekognition collection if it doesn't exist
    aws_handler.create_collection()

    with MongoHandler(db_url, db_name) as mongo_handler:
        logging.info("Executing JXA script to retrieve media items metadata.")
        retrieve_mediaItem_path = "./jxa-scripts/retrieveMediaItemMetadata.js"
        result = execute_jxa_script(retrieve_mediaItem_path)
        if result:
            logging.info("Media items metadata retrieved successfully.")
            metadata = parse_script_output(result)
            if metadata and 'mediaItems' in metadata:
                retrieve_and_store_metadata(metadata['mediaItems'], mongo_handler, collection_name)
                handle_missing_metadata(mongo_handler, collection_name, aws_handler, openai_handler)
            else:
                logging.info("No media items to process.")
        else:
            logging.error("Failed to retrieve media items metadata.")

if __name__ == "__main__":
    main()
