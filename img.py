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
folder_path = os.path.join(current_dir, "json")

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
                        channel_id = item.get('channel_id')
                        dt = datetime.fromisoformat(timestamp) if timestamp else None
                        date_str = dt.strftime("%Y-%m-%d") if dt else None

                        if item.get('attachments'):
                            for attachment in item['attachments']:
                                url = attachment.get('url')
                                # Debug print
                                print(f"Found message with channel_id: {channel_id}")
                                messages.append({
                                    'content': content,
                                    'url': url,
                                    'date_str': date_str,
                                    'dt': dt,
                                    'channel_id': channel_id
                                })
                        else:
                            messages.append({
                                'content': content,
                                'url': None,
                                'date_str': date_str,
                                'dt': dt,
                                'channel_id': channel_id
                            })
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from {filename}: {e}")
    return messages

def download_file(url, file_type, channel_id):
    try:
        print(f"Downloading {file_type} from: {url} for channel: {channel_id}")
        parsed_url = urlparse(url)
        url_hash = hashlib.md5(url.encode()).hexdigest()
        
        # Create channel-specific directory
        if channel_id is None:
            channel_id = 'unknown'
        
        channel_path = os.path.join(media_path, str(channel_id))
        print(f"Creating directory: {channel_path}")  # Debug print
        os.makedirs(channel_path, exist_ok=True)
        
        if file_type == 'image':
            filename = f"{url_hash}.png"
        elif file_type == 'audio':
            filename = f"{url_hash}.mp3"
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

        file_path = os.path.join(channel_path, filename)
        print(f"Will save to: {file_path}")  # Debug print

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
        path = urlparse(url).path.lower()
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
        audio_extensions = {'.mp3', '.wav', '.ogg', '.m4a', '.aac'}
        
        if any(path.endswith(ext) for ext in image_extensions):
            return 'image'
        elif any(path.endswith(ext) for ext in audio_extensions):
            return 'audio'
        return None

def main():
    messages = load_json_files()
    for message in messages:
        url = message.get('url')
        channel_id = message.get('channel_id')
        
        if url:
            print(f"Processing URL: {url} for channel: {channel_id}")  # Debug print
            file_type = get_file_type(url)
            if file_type:
                download_file(url, file_type, channel_id)
            else:
                print(f"Unsupported file type for URL: {url}")

if __name__ == "__main__":
    main()