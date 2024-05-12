import subprocess
import json
import os

def execute_jxa_script(script_path):
    os.makedirs('./outputs', exist_ok=True)

    try:
        process = subprocess.run(['osascript', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if process.stdout:
            parsed_json = json.loads(process.stdout)
            with open('./outputs/output.json', 'w') as f_json:
                json.dump(parsed_json, f_json, indent=4)
            return parsed_json
        else:
            with open('./outputs/output.txt', 'w') as f:
                f.write("STDOUT:\n" + process.stdout + "\nSTDERR:\n" + process.stderr)
            print("No output to parse.")
            return None
    except json.JSONDecodeError:
        with open('./outputs/output.txt', 'w') as f:
            f.write("Failed JSON:\n" + process.stdout + "\nSTDERR:\n" + process.stderr)
        print("Failed to parse JSON output.")
        print("Faulty JSON:", process.stdout)
        return None
    except Exception as e:
        with open('./outputs/output.txt', 'w') as f:
            f.write("Exception occurred:\n" + str(e) + "\nSTDOUT:\n" + process.stdout + "\nSTDERR:\n" + process.stderr)
        print(f"An unexpected error occurred: {e}")
        return None
