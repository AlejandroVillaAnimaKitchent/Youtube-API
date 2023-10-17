# -*- coding: utf-8 -*-
################################################### LIBRARIES ####################################################
import httplib2
import os
import sys
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime as dt
################################################################################################################


#FROM uploader_status
################################################################################################################
def public_status(youtube, video_id):
    print('Trying to set the video public.')
    
    try:
        youtube.videos().update(
          part='contentDetails,status',
          body={
              'id':video_id,
              'status':{'privacyStatus':'public',
                        'selfDeclaredMadeForKids':'True',
                  }
              }).execute()
        print('Success. Video is now public.')
    except HttpError as e:
      print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

  


def program_status(youtube, video_id, publishAt,name):
    print('Trying to set the time for the video.')
    
    try:
        youtube.videos().update(
          part='contentDetails,snippet,status',
          body={
              'id':video_id,
              # 'id':'DEmdkqLhKg4',
              # 'snippet':{'title':'Test Python Public Update'},
              'status':{'privacyStatus':'private',
                        'selfDeclaredMadeForKids':'True',
                         'publishAt':publishAt
                        # 'publishAt':'2022-12-25T12:30:00.000Z'
                  }
              }).execute()
        print('Success. Video will be available at',publishAt)
        with open(f'{name}/logs.txt','a') as logs:
            logs.write('Video will be available at %s ' % publishAt + ', being now: %s \n' % dt.now() ) 
    except HttpError as e:
      print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
      error = 'A retriable HTTP error %d occurred:\n%s' % (e.resp.status,
                                                                     e.content)
      with open(f'{name}/logs.txt','a') as logs:
          logs.write('STATUS ERROR: %s ' % error + ', being now: %s \n' % dt.now() ) 
################################################################################################################

#FROM uploader_thumbs
################################################################################################################
# Call the API's thumbnails.set method to upload the thumbnail image and
# associate it with the appropriate video.
def upload_thumbnail(youtube, video_id, file,name):
    print('Trying to set new thumbnail:')
    try:
      youtube.thumbnails().set(
        videoId=video_id,
        media_body=file).execute()
      print("The custom thumbnail was successfully set.")
      with open(f'{name}/logs.txt','a') as logs:
          logs.write('Custom thumb for %s  successfully set' % video_id + ' at: %s \n' % dt.now() ) 
    except Exception as e:
      print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
      error = 'A retriable HTTP error %d occurred:\n%s' % (e.resp.status,
                                                               e.content)
      with open(f'{name}/logs.txt','a') as logs:
          logs.write('THUMBNAIL ERROR: %s ' % error + ', being now: %s \n' % dt.now() ) 

################################################################################################################
