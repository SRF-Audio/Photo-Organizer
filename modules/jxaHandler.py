import subprocess
import json
import os
import logging

def execute_jxa_script(script_path):
    os.makedirs('./outputs', exist_ok=True)

    try:
        process = subprocess.run(['osascript', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if process.stderr:
            logging.error(f"stderr value detected: {process.stderr}")

        if process.stdout:
            logging.info(f"Stdout value detected successfully.")
            try:
                parsed_json = json.loads(process.stdout)
                with open('./outputs/output.json', 'w') as f_json:
                    json.dump(parsed_json, f_json, indent=4)
                return parsed_json
            except json.JSONDecodeError:
                with open('./outputs/output.txt', 'w') as f:
                    f.write("Failed JSON:\n" + process.stdout + "\nSTDERR:\n" + process.stderr)
                logging.error("Failed to parse JSON output.")
                logging.error("Faulty JSON:", process.stdout)
                return None
        else:
            with open('./outputs/output.txt', 'w') as f:
                f.write("STDOUT:\n" + process.stdout + "\nSTDERR:\n" + process.stderr)
            print("No output to parse.")
            return None
    except Exception as e:
        with open('./outputs/output.txt', 'w') as f:
            f.write("Exception occurred:\n" + str(e) + "\nSTDOUT:\n" + process.stdout + "\nSTDERR:\n" + process.stderr)
        print(f"An unexpected error occurred: {e}")
        return None

def handle_media_export(media_item_id):
    script_template_path = '../jxa-scripts/exportMediaItem.js.tpl'
    script_path = '../jxa-scripts/exportMediaItem.js'
    
    try:
        with open(script_template_path, 'r') as template_file:
            script_content = template_file.read().replace('{{mediaItemId}}', media_item_id)
        
        with open(script_path, 'w') as script_file:
            script_file.write(script_content)
        
        result = execute_jxa_script(script_path)
        
        os.remove(script_path)
        
        if result and 'path' in result:
            return result['path']
        elif result and 'error' in result:
            logging.error(f"Error exporting media item: {result['error']}")
            return None
        else:
            logging.error("Unknown error occurred during media export.")
            return None
    except Exception as e:
        logging.error(f"Exception in handle_media_export: {e}")
        return None
