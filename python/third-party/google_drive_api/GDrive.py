from __future__ import print_function
import sys
import io
import pip
import httplib2
import os
from mimetypes import MimeTypes



try:
	from googleapiclient.errors import HttpError
	from apiclient import discovery
	import oauth2client
	from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
	from oauth2client import client
	from oauth2client import tools
except ImportError:
    print('goole-api-python-client is not installed. Try:')
    print('sudo pip install --upgrade google-api-python-client')
    sys.exit(1)
import sys


class Flag:
    auth_host_name = 'localhost'
    noauth_local_webserver = False
    auth_host_port = [8080, 8090]
    logging_level = 'ERROR'


try:
    import argparse

    # flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    flags = Flag()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'gdrive_client_secret.json'
APPLICATION_NAME = 'GDrive'



def get_credentials():

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        # if flags:
        credentials = tools.run_flow(flow, store, flags)
        # else:  # Needed only for compatibility with Python 2.6
        #     credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def upload(path, parent_id=None):
    mime = MimeTypes()
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    file_metadata = {
        'name': os.path.basename(path),
        # 'mimeType' : 'application/vnd.google-apps.spreadsheet'
    }
    if parent_id:
        file_metadata['parents'] = [parent_id]

    media = MediaFileUpload(path,
                            mimetype=mime.guess_type(os.path.basename(path))[0],
                            resumable=True)
    try:
        file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
    except HttpError:
        print('corrupted file')
        pass
    print(file.get('id'))


def share(file_id, email):
    def callback(request_id, response, exception):
        if exception:
            # Handle error
            print(exception)
        else:
            print(response.get('id'))

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    batch = service.new_batch_http_request(callback=callback)
    user_permission = {
        'type': 'user',
        'role': 'reader',
        'emailAddress': email
    }
    batch.add(service.permissions().create(
        fileId=file_id,
        body=user_permission,
        fields='id',
    ))
    batch.execute()


def listfiles():
    results = service.files().list(fields="nextPageToken, files(id, name,mimeType)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        print('Filename (File ID)')
        for item in items:
            print('{0} ({1})'.format(item['name'].encode('utf-8'), item['id']))
        print('Total=', len(items))

def delete(fileid):
    service.files().delete(fileId=fileid).execute()


def download(file_id, path=os.getcwd()):
    request = service.files().get_media(fileId=file_id)
    name = service.files().get(fileId=file_id).execute()['name']
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(int(status.progress() * 100))
    f = open(path + '/' + name, 'wb')
    f.write(fh.getvalue())
    print('File downloaded at', path)
    f.close()


def createfolder(folder, recursive=False):
    if recursive:
        print('recursive ON')
        ids = {}
        for root, sub, files in os.walk(folder):
            par = os.path.dirname(root)

            file_metadata = {
                'name': os.path.basename(root),
                'mimeType': 'application/vnd.google-apps.folder'
            }
            if par in ids.keys():
                file_metadata['parents'] = [ids[par]]
            print(root)
            file = service.files().create(body=file_metadata,
                                          fields='id').execute()
            id = file.get('id')
            print(id)
            ids[root] = id
            for f in files:
                print(root+'/'+f)
                upload(root + '/' + f, id)
    else:
        print('recursive OFF')
        file_metadata = {
                'name': os.path.basename(folder),
                'mimeType': 'application/vnd.google-apps.folder'
            }
        file = service.files().create(body=file_metadata,
                                          fields='id').execute()
        print(file.get('id'))

if __name__ == '__main__':
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    method = sys.argv[1]
    if method == 'upload':
        if os.path.isdir(sys.argv[2]):
            if len(sys.argv) == 4 and sys.argv[3] == 'R':
                createfolder(sys.argv[2], True)
            else:
                createfolder(os.path.basename(sys.argv[2]))

        else:
            upload(sys.argv[2])
    elif method == 'list':
        listfiles()
    elif method == 'delete':
        delete(sys.argv[2])
    elif method == 'download':
        download(sys.argv[2], sys.argv[3])
    elif method == 'share':
    	share(sys.argv[2], sys.argv[3])
    elif method == 'folder':
        createfolder(sys.argv[2])
    elif method == 'debug':
        print(os.getcwd())
