# -*- coding: utf-8 -*-
########################################## LIBRARIES ##########################################
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from m4k_status import program_status
import pickle as pkl

############## FOR OUTER FUNCTIONS ##############
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
#################################################

###############################################################################################


###############################################################################################

###################################### AUTH & SCOPES ##########################################
CLIENT_SECRETS_FILE = 'client_secret_anima.json'

SCOPES = [
           'https://www.googleapis.com/auth/youtube',                                # Thumb  
           'https://www.googleapis.com/auth/youtubepartner-content-owner-readonly',  # ContentID  
          'https://www.googleapis.com/auth/youtubepartner',                         # ? 
           'https://www.googleapis.com/auth/youtube.force-ssl',                      # Programar
          'https://www.googleapis.com/auth/youtube.readonly']                       # Ver livestreams activos

SCOPES_PARTNER = [
          'https://www.googleapis.com/auth/youtubepartner',                         # ? 
          'https://www.googleapis.com/auth/youtube.readonly']                       # Ver livestreams activos

API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
API_SERVICE_NAME_PARTNER = 'youtubePartner'
API_VERSION_PARTNER = 'v1'

###############################################################################################


############################################ FUNCTIONS ########################################



# Authorize the request and store authorization credentials.
########################################
def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server()
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials), credentials
########################################

# Save the authorized service so it doesn't request a code again.
########################################
def save_authenticated_service(youtube):
    with open('anima_auth_service.pkl', 'wb') as file: 
        pkl.dump(youtube, file)
########################################

# Save the authorized credentials so it doesn't request a code again.
########################################
def save_authenticated_credentials(credentials):
    with open('anima_auth_credentials.pkl', 'wb') as file: 
        pkl.dump(credentials, file)
########################################

# Load credentials.
########################################
def load_credentials():
    with open('anima_auth_credentials.pkl', 'rb') as file: 
        credentials = pkl.load(file)
    return credentials
########################################

# Load said service.
########################################
def load_authenticated_service():
    with open('anima_auth_service.pkl', 'rb') as file: 
        youtube = pkl.load(file)
    return youtube
########################################

# Load scredentials to create service.
########################################
def load_credentials_service(credentials):
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
########################################


# Authorize the request and store partnered credentials.
########################################
def get_partnered_service():
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server()
    return build(API_SERVICE_NAME_PARTNER, API_VERSION_PARTNER, credentials=credentials,static_discovery=False), credentials
########################################

# Save the authorized service so it doesn't request a code again.
########################################
def save_partnered_service(youtubePartner):
    with open('anima_partner_service.pkl', 'wb') as file: 
        pkl.dump(youtubePartner, file)
########################################

# Save the authorized credentials so it doesn't request a code again.
########################################
def save_partnered_credentials(credentialsPartner):
    with open('anima_partner_credentials.pkl', 'wb') as file: 
        pkl.dump(credentialsPartner, file)
########################################

# Load credentials.
########################################
def load_partner():
    with open('anima_partner_credentials.pkl', 'rb') as file: 
        credentialsPartner = pkl.load(file)
    return credentialsPartner
########################################

# Load said service.
########################################
def load_partnered_service():
    with open('anima_partner_service.pkl', 'rb') as file: 
        youtubePartner = pkl.load(file)
    return youtubePartner
########################################

# Load scredentials to create service.
########################################
def load_partner_service(credentialsPartner):
    return build(API_SERVICE_NAME_PARTNER, API_VERSION_PARTNER, credentials=credentialsPartner,static_discovery=False)
########################################


###############################################################################################
if __name__ == "__main__":
    
    youtube, credentials = get_authenticated_service()
    save_authenticated_service(youtube)
    save_authenticated_credentials(credentials)
    youtube = load_authenticated_service()
    credentials = load_credentials()
    youtube = load_credentials_service(credentials)
    
    
    youtubePartner, credentialsPartner = get_partnered_service()
    save_partnered_service(youtubePartner)
    save_partnered_credentials(credentialsPartner)
    youtubePartner = load_partnered_service()
    credentialsPartner = load_partner()
    youtubePartner = load_partner_service(credentialsPartner)
    
    
    channelId = 'UCkKFMspQtSicDP-l7Nu841A' #HelloBaby
    channelName = 'Hello Baby! Aprende Inglés con Cuquín' #CCENG
    contentOwner = 'iHywrp4i6tV0ZP3a3-_GZA' # Anima
    offset, duration = 0, 30
    cueType = 'cueTypeAd'
    

    # Hacerlo made for kids
    request = youtube.liveBroadcasts().list(
        part="id,snippet,status,contentDetails",
        broadcastStatus="upcoming",
        broadcastType="all",
        onBehalfOfContentOwner=contentOwner,
        onBehalfOfContentOwnerChannel=channelId
    )
    liveBroadcasts = request.execute() # Get active broadcasts
    
    broadcast_ids = [item['id'] for item in liveBroadcasts['items']] # Get active broadcasts

    
    if len(broadcast_ids)>0:
        for broadcast_id in broadcast_ids: 
            program_status(youtube=youtube, video_id=broadcast_id)
            
    
    videoId = broadcast_ids[-1]
    
    # Habilitar monetización
    request = youtubePartner.claimSearch().list(
      videoId= videoId
    )
    assets = request.execute()
    assetIds = [item['assetId'] for item in assets['items']]
    
    assetId = assetIds[0]
    # request = youtubePartner.policies().list( )
    # policies = request.execute()
    

    policy = dict(
      rules=[dict(
        action="monetize"
      )]
    )
  
    body = dict(
      assetId=assetId,
      videoId=videoId,
      policy=policy,
      contentType="audiovisual"
    )
    
    youtubePartner.claims().insert(
      onBehalfOfContentOwner='iHywrp4i6tV0ZP3a3-_GZA',
      body=body
    ).execute()
    
    body = dict(
      adFormats=["trueview_instream",'overlay','standard_instream']
    )
    
    youtubePartner.videoAdvertisingOptions().update(
      videoId=videoId,
      onBehalfOfContentOwner='iHywrp4i6tV0ZP3a3-_GZA',
      body=body
    ).execute()

###############################################################################################
