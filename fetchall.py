"""
Shows basic usage of the Photos v1 API.

Creates a Photos v1 API service and prints the names and ids of the last 10 albums
the user has access to.
"""
import pandas as pd
import os 
import datetime
import pickle
import json
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
	
def get_creds():
    # Setup the Photo v1 API
    SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']
    creds = None
    if(os.path.exists("token.pickle")):
        with open("token.pickle", "rb") as tokenFile:
            creds = pickle.load(tokenFile)
    if not creds or not creds.valid:
        if (creds and creds.expired and creds.refresh_token):
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(
                host='127.0.0.1',
                port=8000,
            )
        with open("token.pickle", "wb") as tokenFile:
            pickle.dump(creds, tokenFile)
    return creds

def main():
    creds = get_creds()
    service = build('photoslibrary', 'v1', credentials = creds,static_discovery=False)
    
    mylist = []
    page_photos = service.mediaItems().list(pageSize=99).execute()
    while True:
        nextPageToken = page_photos['nextPageToken']
        for x in page_photos['mediaItems']:
            myitem = dict(
                productUrl=x['productUrl'],
                filename=x['filename'],
            )
            mediaMetadata = dict(x['mediaMetadata'])
            extra = None
            for k in ['video','photo']:
                if k in mediaMetadata.keys():
                    extra = mediaMetadata.pop(k)

            myitem.update(mediaMetadata)
            if extra:
                myitem.update(extra)
            
            mylist.append(myitem)

        df = pd.DataFrame(mylist)
        df.to_csv('all.csv',index=False)
        df.creationTime = datetime.datetime.strptime(x,'%Y-%m-%dT%H:%M:%SZ')

        page_photos = service.mediaItems().list(
                            pageSize=99, pageToken=nextPageToken).execute()
        if 'nextPageToken' in page_photos.keys():
            nextPageToken = page_photos['nextPageToken']
        else:
            break

if __name__ == '__main__':
    main()
