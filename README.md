# photo-organizer

## Original LLM Prompt

I'm creating a Python utility called "photo-organizer" that will handle automated title, description, and keyword tagging for my Apple Photos library. I'll be using MongoDB in a Docker Container, and Python will be the execution core. 

To interact with Photos, photo-organizer will use the subprocess module to call JXA scripts that interact with Photos, and then return results to stdout.

I've already got the first JXA script working, so now we're going to start on the Python core. 

I want the application to be modular, maintainable, robust, and it should explicitly handle errors. 

## Overview

The application will consist of several Python modules, each responsible for a specific part of the system's functionality:

- main.py: Core controller of the application, coordinating the interactions between the other modules.
- jxaHandler.py: Manages the execution of JXA scripts, interacting with the Apple Photos library.
- mongoHandler.py: Handles all interactions with MongoDB for storing and retrieving photo metadata.
- apiHandler.py: Centralized API request and response management, including error handling and logging.
- awsHandler.py: Interacts with AWS Rekognition for automated photo tagging.
- openAiHandler.py: Utilizes OpenAI's Vision API to enrich photo descriptions post-Rekognition analysis.

## Detailed Module Design

### main.py

Orchestrates the application flow.
Manages module interactions and handles high-level exceptions.

### jxaHandler.py

Executes JXA scripts using subprocess.
Parses and returns results from stdout.
Handles errors specifically related to JXA script execution.

### mongoHandler.py

Establishes and maintains the MongoDB connection.
Implements CRUD operations for photo metadata.
Handles database-related exceptions.

### apiHandler.py

Standardizes API interactions.
Implements common request-response patterns.
Manages logging and centralized error handling.

### awsHandler.py

Interfaces with AWS Rekognition.
Handles API calls and processes responses.
Manages errors and retries for AWS services.

### openAiHandler.py

Communicates with OpenAI Vision API.
Processes and enhances descriptions based on AI analysis.
Handles API-specific errors and data parsing.

## Error Handling

Each module will include robust error handling to manage and log exceptions specific to their operations.
The main.py will handle any uncaught exceptions from the modules, ensuring the application can gracefully recover or terminate.