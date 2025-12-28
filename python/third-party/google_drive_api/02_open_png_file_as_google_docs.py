#!/usr/bin/env python3
import io

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from httplib2 import Http
from oauth2client import file, client, tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

#todo: 잘 안됨

# SCOPES = ['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive.metadata.readonly']
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
store = file.Storage('storage.json')
creds = store.get()

if not creds or creds.invalid:
    print("make new storage data file ")
    flow = client.flow_from_clientsecrets('client_secret_drive.json', SCOPES)
    creds = tools.run_flow(flow, store, flags) \
        if flags else tools.run(flow, store)

DRIVE = build('drive', 'v3', http=creds.authorize(Http()))

results = DRIVE.files().list(
    q="name contains '1-' and name contains 'png'",
    spaces='drive',
    pageSize=10,
    fields="nextPageToken, files(id, name)").execute()
items = results.get('files', [])

if not items:
    print('No files found.')
else:
    print('Files:')
    for item in items:
        print(u'{0} ({1})'.format(item['name'], item['id']))

        request = DRIVE.files().export_media(fileId=item['id'],
                                               mimeType='application/vnd.oasis.opendocument.text')
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
