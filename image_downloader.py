import os
import json
import requests
from io import BytesIO
from datetime import datetime
from PIL import Image
from urllib.parse import urlparse
import hashlib
import mimetypes

# Set paths relative to the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
media_path = os.path.join(current_dir, "media")
folder_path = os.path.join(current_dir, "temp")

# Ensure media directory exists
os.makedirs(media_path, exist_ok=True)

def load_json_files():
    messages = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                try:
                    data = json.load(file)
                    for item in data:
                        content = item.get('content')
                        timestamp = item.get('timestamp')
                        dt = datetime.fromisoformat(timestamp) if timestamp else None
                        date_str = dt.strftime("%Y-%m-%d") if dt else None

                        if item.get('attachments'):
                            for attachment in item['attachments']:
                                url = attachment.get('url')
                                messages.append((content, url, date_str, dt))
                        else:
                            messages.append((content, None, date_str, dt))
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from {filename}: {e}")
    return messages

def download_file(url, file_type):
    try:
        print(f"Downloading {file_type} from: {url}")
        parsed_url = urlparse(url)
        url_hash = hashlib.md5(url.encode()).hexdigest()
        
        if file_type == 'image':
            filename = f"{url_hash}.png"
        elif file_type == 'audio':
            filename = f"{url_hash}.mp3"
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

        file_path = os.path.join(media_path, filename)

        if os.path.exists(file_path):
            print(f"File already exists: {file_path}")
            return file_path

        response = requests.get(url)
        response.raise_for_status()

        with open(file_path, 'wb') as file:
            file.write(response.content)

        print(f"File saved to: {file_path}")
        return file_path
    except Exception as e:
        print(f"Error downloading {file_type}: {e}")
        return None

def get_file_type(url):
    content_type, _ = mimetypes.guess_type(url)
    if content_type:
        if content_type.startswith('image'):
            return 'image'
        elif content_type.startswith('audio'):
            return 'audio'
    return None

def main():
    messages = load_json_files()
    for content, url, date_str, dt in messages:
        if url:
            file_type = get_file_type(url)
            if file_type:
                download_file(url, file_type)
            else:
                print(f"Unsupported file type for URL: {url}")

if __name__ == "__main__":
    main()
