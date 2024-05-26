import os
import subprocess
import json
import logging

def execute_jxa_script(script_path):
    try:
        process = subprocess.run(['osascript', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if process.stderr:
            logging.error(f"stderr value detected: {process.stderr}")
        logging.debug(f"JXA script output: {process.stdout}")
        return process.stdout
    except Exception as e:
        logging.error(f"Exception occurred during script execution: {e}")
        return None

def parse_script_output(output):
    try:
        parsed_output = json.loads(output)
        logging.debug(f"Parsed script output: {parsed_output}")
        return parsed_output
    except json.JSONDecodeError:
        logging.error("Failed to parse JSON output.")
        return None

def generate_jxa_script(template_path, script_path, media_item_id):
    try:
        with open(template_path, 'r') as template_file:
            script_content = template_file.read().replace('{{mediaItemId}}', media_item_id)
        with open(script_path, 'w') as script_file:
            script_file.write(script_content)
    except Exception as e:
        logging.error(f"Exception in generate_jxa_script: {e}")
        raise

def find_file_in_directory(directory, base_filename):
    for file in os.listdir(directory):
        if os.path.splitext(file)[0] == base_filename:
            return os.path.join(directory, file)
    return None

def handle_media_export(media_item_id):
    script_template_path = '/Users/stephenfroeber/GitHub/Photo-Organizer/jxa-scripts/exportMediaItem.js.tpl'
    script_path = '/Users/stephenfroeber/GitHub/Photo-Organizer/jxa-scripts/temp_scripts/exportMediaItem.js'
    try:
        generate_jxa_script(script_template_path, script_path, media_item_id)
        result_output = execute_jxa_script(script_path)
        result = parse_script_output(result_output)
        if result and 'path' in result:
            base_filename = os.path.basename(result['path'])
            export_directory = os.path.dirname(result['path'])
            export_path = find_file_in_directory(export_directory, base_filename)
            if export_path and os.path.exists(export_path):
                os.remove(script_path)
                return export_path
            else:
                logging.error(f"Exported file not found: {result['path']}")
        logging.error(f"Error exporting media item: {result.get('error', 'Unknown error')}")
        return None
    except Exception as e:
        logging.error(f"Exception in handle_media_export: {e}")
        return None

def delete_exported_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logging.info(f"Deleted file: {file_path}")
        else:
            logging.warning(f"File not found for deletion: {file_path}")
    except Exception as e:
        logging.error(f"Failed to delete file: {file_path}, due to: {e}")