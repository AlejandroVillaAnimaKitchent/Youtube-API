################################################################
import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
#####################################################################

scopes = ["https://www.googleapis.com/auth/youtube"]

#############################################################################
# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
#############################################################################

#############################################################################
api_service_name = "youtubeAnalytics"
api_version = "v2"
client_secrets_file = "client_secret_anima.json"
#############################################################################


# Get credentials and create an API client
#############################################################################
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)
credentials = flow.run_local_server()
youtube_analytics = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)
#############################################################################

#Main Function 
#############################################################################
def add_videos_to_group(group_id, video_ids):
    for video_id in video_ids:
        
        request = youtube_analytics.groupItems().insert(
            body={
              "groupId": group_id,
              "resource": {
                "kind": "youtube#video",
                "id": video_id
              }
            }
        )
        response = request.execute()

   #print(response)
#############################################################################

#############################################################################
if __name__ == "__main__":
 
#An example to prove     
    group_id = "SdBy0sVhWqk"
    video_ids = ['fAdCIGWOi-A', 'E_gA3YiWZkM', 'hwWOitlu2jc', 'Af5Um0X8Qo4', 'kItEjWOl2g8']
    add_videos_to_group(group_id, video_ids)
    
#############################################################################
