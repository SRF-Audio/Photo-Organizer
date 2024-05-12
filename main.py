from modules.jxaHandler import execute_jxa_script

def main():
    retrieve_mediaItem_path = "./jxa-scripts/retrieveMediaItemIds.js"
    result = execute_jxa_script(retrieve_mediaItem_path)
    if result:
        print("Script executed successfully:")
        print(result)
    else:
        print("Script execution failed.")

if __name__ == "__main__":
    main()
