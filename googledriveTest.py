# Using Python Google Drive API
# https://developers.google.com/drive/api/quickstart/python
# Up/Downloads owned by https://www.geeksforgeeks.org/upload-and-download-files-from-google-drive-storage-using-python/
from __future__ import print_function

import os.path
import io
import shutil
import time

from mimetypes import MimeTypes

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

# If modifying these scopes, delete the file GD_token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

#5MB.bin (1xRb-nXRJpNsLfahsfchfk6qHryzmTndS)
#50MB.bin (1Z6Bj9T_NmKmROzfwkQUuPj4mz82OXSj-)


def AccessGoogleDrive():
    creds = None
    # The file GD_token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('GD_token.json'):
        creds = Credentials.from_authorized_user_file('GD_token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'GD_credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('GD_token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')

    return service


def printFiles(service):
    try:
        # Call the Drive v3 API
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


def uploadFile(service, filename):

    # Find the MimeType of the file
    mimetype = MimeTypes().guess_type(filename)[0]

    # create file metadata
    file_metadata = {'name': filename, "parents": ["13lvylFilSZ2Wt52A-OisL_fa_H1BmW2H"]}

    media = MediaFileUpload("UploadLocal/"+filename, mimetype=mimetype)

    # Create a new file in the Drive storage
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()


def downloadFile(service, fileid, filename):
    request = service.files().get_media(fileId=fileid)
    fh = io.BytesIO()

    # Initialise a downloader object to download the file
    downloader = MediaIoBaseDownload(fh, request)
    done = False

    # Download the data in chunks
    while not done:
        done = downloader.next_chunk()

    fh.seek(0)
    # Write the received data to the file
    file_handle = open("DownloadLocal/"+filename, 'wb')
    shutil.copyfileobj(fh, file_handle)


def main(filename, id):
    f = open("AccessStats.txt", 'a', encoding='utf-8')
    f.write("GoogleDrive,")

    service = AccessGoogleDrive()

    start = time.perf_counter()
    uploadFile(service, filename)
    end = time.perf_counter() - start
    print("Upload " + filename + " : " + '%.6f' % end + ",")
    f.write("" + '%.6f' % end + ",")

    start = time.perf_counter()
    downloadFile(service, id, filename)
    end = time.perf_counter() - start
    print("Download " + filename + " : " + '%.6f' % end + ",")
    f.write("" + '%.6f' % end + ",")


if __name__ == '__main__':
    main("5MB.bin", '1xRb-nXRJpNsLfahsfchfk6qHryzmTndS')
    main("50MB.bin", '1Z6Bj9T_NmKmROzfwkQUuPj4mz82OXSj-')
