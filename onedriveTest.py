# Using Microsoft Graph API for Python (Python Quickstart)
# https://developer.microsoft.com/en-us/graph/quick-start
# Access Code owned by https://learndataanalysis.org/about-me/

import time
import requests
from ms_graph import generate_access_token, GRAPH_API_ENDPOINT


def accessOneDrive():
    APP_ID = ''    #YOUR APP ID
    SCOPES = ['Files.ReadWrite']

    access_token = generate_access_token(APP_ID, SCOPES)
    access = {
        'Authorization': 'Bearer ' + access_token['access_token']
    }
    return access


def uploadFile(access, filename):
    file_handle = open("UploadLocal/"+filename, 'r+b')
    requests.put(
        GRAPH_API_ENDPOINT + f'/me/drive/items/root:/UploadOnedrive/{filename}:/content',
        headers=access,
        data=file_handle.read()
    )
    file_handle.close()


def downloadFile(access, filename, fileid):
    file_handle = open("DownloadLocal/" + filename, 'w+b')
    response_file_content = requests.get(GRAPH_API_ENDPOINT + f'/me/drive/items/{fileid}/content', headers=access)
    file_handle.write(response_file_content.content)
    file_handle.close()


def main(filename, id):
    f = open("AccessStats.txt", 'a', encoding='utf-8')
    f.write("OneDrive,")

    access = accessOneDrive()

    start = time.perf_counter()
    uploadFile(access, filename)
    end = time.perf_counter() - start
    print("Upload " + filename + " : " + '%.6f' % end + ",")
    f.write("" + '%.6f' % end + ",")

    start = time.perf_counter()
    downloadFile(access, filename, id)
    end = time.perf_counter() - start
    print("Download " + filename + " : " + '%.6f' % end + ",")
    f.write("" + '%.6f' % end + ",")


if __name__ == '__main__':
    main("5MB.bin", "98117D10CBE992ED!117")
    main("50MB.bin", "98117D10CBE992ED!118")
