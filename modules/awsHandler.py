import boto3
import logging
import os
from botocore.exceptions import BotoCoreError, ClientError

class AWSHandler:
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name, collection_id):
        self.rekognition_client = boto3.client(
            'rekognition',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )
        self.collection_id = os.getenv('REKOGNITION_COLLECTION_ID')

    def create_collection(self):
        try:
            response = self.rekognition_client.create_collection(CollectionId=self.collection_id)
            logging.info(f"Created collection {self.collection_id}: {response['StatusCode']}")
        except (BotoCoreError, ClientError) as error:
            logging.error(f"Error creating collection: {error}")

    def delete_collection(self):
        try:
            response = self.rekognition_client.delete_collection(CollectionId=self.collection_id)
            logging.info(f"Deleted collection {self.collection_id}: {response['StatusCode']}")
        except (BotoCoreError, ClientError) as error:
            logging.error(f"Error deleting collection: {error}")

    def index_faces(self, photo_path):
        try:
            with open(photo_path, 'rb') as image_file:
                response = self.rekognition_client.index_faces(
                    CollectionId=self.collection_id,
                    Image={'Bytes': image_file.read()},
                    ExternalImageId=photo_path,
                    DetectionAttributes=['ALL']
                )
            face_records = response['FaceRecords']
            logging.info(f"Indexed faces for {photo_path}: {face_records}")
            return face_records
        except (BotoCoreError, ClientError) as error:
            logging.error(f"Error indexing faces: {error}")
            return []

    def detect_faces(self, photo_path):
        try:
            with open(photo_path, 'rb') as image_file:
                response = self.rekognition_client.detect_faces(
                    Image={'Bytes': image_file.read()},
                    Attributes=['ALL']
                )
            face_details = response['FaceDetails']
            logging.info(f"Detected faces for {photo_path}: {face_details}")
            return face_details
        except (BotoCoreError, ClientError) as error:
            logging.error(f"Error detecting faces: {error}")
            return []

    def search_faces_by_image(self, photo_path, max_faces=5):
        try:
            with open(photo_path, 'rb') as image_file:
                response = self.rekognition_client.search_faces_by_image(
                    CollectionId=self.collection_id,
                    Image={'Bytes': image_file.read()},
                    MaxFaces=max_faces
                )
            face_matches = response['FaceMatches']
            logging.info(f"Found face matches for {photo_path}: {face_matches}")
            return face_matches
        except (BotoCoreError, ClientError) as error:
            logging.error(f"Error searching faces: {error}")
            return []


    def detect_labels(self, photo_path):
        try:
            logging.debug(f"Attempting to open file: {photo_path}")
            if not os.path.exists(photo_path):
                logging.error(f"File not found: {photo_path}")
                return []
                
            with open(photo_path, 'rb') as image_file:
                response = self.rekognition_client.detect_labels(
                    Image={'Bytes': image_file.read()},
                    MaxLabels=10,
                    MinConfidence=75
                )
            labels = [label['Name'] for label in response['Labels']]
            logging.info(f"Detected labels for {photo_path}: {labels}")
            return labels
        except (BotoCoreError, ClientError) as error:
            logging.error(f"Error in AWS Rekognition: {error}")
            return []
        except FileNotFoundError as fnf_error:
            logging.error(f"File not found error: {fnf_error}")
            return []
