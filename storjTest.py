# Using Storj - Third Party: Uplink Python
# https://github.com/storj-thirdparty/uplink-python

import time
from uplink_python.uplink import Uplink


MY_API_KEY = ""    #YOUR API KEY
MY_SATELLITE = "12L9ZFwhzVpuEKMUNUqkaTLGzwY9G24tbiigLiXpmZWKwmcNDDs@eu1.storj.io:7777"
MY_ENCRYPTION_PASSPHRASE = ""   #YOUR ENCRYPTION PHRASE
BUCKET_NAME = "load-bucket"


def uploadFile(project, filename):
    file_handle = open("UploadLocal/"+filename, 'r+b')
    upload = project.upload_object(BUCKET_NAME, "UploadStorj/"+filename)
    upload.write_file(file_handle)
    upload.commit()
    file_handle.close()


def downloadFile(project, filename):
    file_handle = open("DownloadLocal/"+filename, 'w+b')
    download = project.download_object(BUCKET_NAME, "DownloadStorj/"+filename)
    download.read_file(file_handle)
    download.close()
    file_handle.close()


def main(filename):
    f = open("AccessStats.txt", 'a', encoding='utf-8')
    f.write("StorJ,")

    uplink = Uplink()

    access = uplink.request_access_with_passphrase(MY_SATELLITE, MY_API_KEY, MY_ENCRYPTION_PASSPHRASE)
    project = access.open_project()

    start = time.perf_counter()
    uploadFile(project, filename)
    end = time.perf_counter() - start
    print("Upload "+filename+" : " + '%.6f' % end + ",")
    f.write("" + '%.6f' % end + ",")

    start = time.perf_counter()
    downloadFile(project, filename)
    end = time.perf_counter() - start
    print("Download "+filename+" : " + '%.6f' % end + ",")
    f.write("" + '%.6f' % end + ",")

    project.close()


if __name__ == '__main__':
    main("5MB.bin")
    main("50MB.bin")
