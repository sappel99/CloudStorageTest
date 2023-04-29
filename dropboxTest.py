# Using Python SDK for API v2
# https://www.dropbox.com/developers/documentation/python#tutorial

import time
import dropbox
from dropbox.files import WriteMode


def accessDropBox():
    dbx = dropbox.Dropbox('sl.')    #YOUR API ACCESS
    #print(dbx.users_get_current_account())
    return dbx


def uploadFile(dbx, filename, x):
    file_handle = open("UploadLocal/"+filename, 'r+b')
    if x % 2:
        dbx.files_upload(file_handle.read(), "/UploadDropbox/"+filename, mode=WriteMode.overwrite)
    else:
        dbx.files_upload(file_handle.read(), "/UploadDropbox/"+filename, mode=WriteMode.overwrite, mute=True)
    file_handle.close()


def downloadFile(dbx, filename):
    file_handle = open("DownloadLocal/"+filename, 'w+b')
    md, res = dbx.files_download("/DownloadDropbox/"+filename)
    file_handle.write(res.content)
    file_handle.close()


def main(filename):
    f = open("AccessStats.txt", 'a', encoding='utf-8')
    f.write("DropBox,")

    dbx = accessDropBox()

    start = time.perf_counter()
    uploadFile(dbx, filename, 0)
    end = time.perf_counter() - start
    print("Upload "+filename+" : " + '%.6f' % end + ",")
    f.write("" + '%.6f' % end + ",")

    start = time.perf_counter()
    downloadFile(dbx, filename)
    end = time.perf_counter() - start
    print("Download "+filename+" : " + '%.6f' % end + ",")
    f.write("" + '%.6f' % end + ",")

    dbx.close()


if __name__ == '__main__':
    main("5MB.bin")
    main("50MB.bin")
