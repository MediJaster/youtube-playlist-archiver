import os, json
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("API_KEY")

directory_files = os.listdir(os.getenv("DOWNLOAD_DIR"))
print(directory_files)

import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def get_playlist_items(playlist_id, page_id=None):
    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=key)

    request = youtube.playlistItems().list(
        part = "snippet, contentDetails",
        maxResults = 30,
        playlistId = playlist_id,
        pageToken = page_id,
    )

    return request.execute()

saved_playlists = {}

try:
    with open("saved_playlists.json", "r") as json_file:
        saved_playlists = json.load(json_file)
        json_file.close()

except FileNotFoundError:
    json_file = open("saved_playlists.json", "w")
    json.dump({}, json_file)
    json_file.close()

def main():
    playlist_ids = ["PLCvPrFTfR1h4ZRcYgRSEdo7Rx9fq5GzMI", "PLCvPrFTfR1h6ARHTeh6AeWrChhPSad3-w"]

    for playlist_id in playlist_ids:
        
        page_id = ""
        items = []

        while page_id is not None:
            response = get_playlist_items(playlist_id, page_id)

            for item in response["items"]:

                title = item["snippet"]["title"]

                if title != "Deleted video":

                    id = item["contentDetails"]["videoId"]
                    url = f"https://www.youtube.com/watch?v={id}"

                    item_dict = {
                        "id" : id,
                        "url" : url,
                        "title" : title
                    }

                    items.append(item_dict)


            try:
                page_id = response["nextPageToken"]

            except KeyError:
                page_id = None
                break
        
        saved_playlists[playlist_id] = {
            "item_count" : len(items),
            "items" : []
        }
        saved_playlists[playlist_id]["items"] = items


    with open("saved_playlists.json", "w") as json_file:
        json.dump(saved_playlists, json_file)
        json_file.close()



if __name__ == "__main__":
    main()