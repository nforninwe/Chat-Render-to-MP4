import json
from datetime import datetime

def parse_and_display_chat(json_data):
    """
    Parses chat data from a JSON string 

    Args:
        json_data (str): A string containing the chat data in JSON format.
    """
    try:
        # Load the JSON from string
        data = json.loads(json_data)
        chat_messages = data.get("chat", [])

        if not chat_messages:
            print("No chat messages found.")
            return

        print("--- Chat History ---")
        print("-" * 20)

        # Iterate through each message in the list
        for message in chat_messages:
            sender = message.get("sender", "Unknown Sender")
            text = message.get("message", "No message content.")
            timestamp_str = message.get("timestamp", "")

            if timestamp_str:
                dt_object = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                formatted_time = dt_object.strftime('%Y-%m-%d %I:%M %p')
            else:
                formatted_time = "No timestamp"

            print(f"[{formatted_time}] {sender}: {text}")


    except json.JSONDecodeError:
        print("Error: Invalid JSON data provided.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Read the JSON file as a string
    with open('data.json', 'r', encoding='utf-8') as file:
        json_str = file.read()
    parse_and_display_chat(json_str)