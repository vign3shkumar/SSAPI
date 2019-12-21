import hashlib, time, uuid, os, shutil, re
from datetime import datetime


def get_datetime():
    return datetime.now().strftime("%d%m%y%H%M%S")


def get_time():
    return str(int(time.time()))

def get_uuid():
    return str(uuid.uuid1())

def get_buildid():
    return '{831419BC-6BCA-44C5-A01A-1C614E1E15DD}'


def createDir(path, f_del=None):

    try:
        os.mkdir(path)
        return  path
    except FileExistsError:
        if f_del :
            if delete_all_files(path):
                os.mkdir(path)
                return path

    return None

def delete_all_files(path):
    try:
        shutil.rmtree(path, ignore_errors=False)
        return True
    except:
        pass
    return False

def get_sha256(filepath, filesize):
    sha_256 = hashlib.sha256()
    sha_256.update(str(filesize).encode())
    sha_256.update(filepath.encode('utf-8'))
    return  sha_256.hexdigest()

def get_sha256_file(filepath):
    sha2 = hashlib.sha256()
    with open(filepath,'rb') as h_shafile:
        while True:
            data = h_shafile.read(8192)
            if not data:
                break
            sha2.update(data)
    return sha2.hexdigest()

def filename_frmpath(path):
    sha256_ptrn = re.compile('[0-9a-fA-F]{64}')
    sha256_mtch = sha256_ptrn.search(path)
    if sha256_mtch != None:
        return sha256_mtch.group()
    return None