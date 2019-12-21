import  random, string, os, zipfile, name, utility


def randomFilename(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def get_signer():
    return  random.choice(name.signers)


def get_file_size():
    return random.randint(100,999999)


def createFiles(path, fileCnt, scan_entries):

    fileextns = [".exe",".dll",".drv",".sys",".acm",".ax",".cpl",".efi",".ocx",".scr"]

    if path.find("\\WinSxS\\") > 0:
        fileextns = [".dll",".exe"]

    elif path.find("\\drivers\\") > 0:
        fileextns = [".sys"]

    elif path.find("\\Program Files\\") > 0:
        fileextns = [".dll",".exe"]

    elif path.find("\\system32\\") > 0:
        fileextns = [".exe",".dll",".drv",".efi",".ocx"]

    for extn in fileextns:
        for i in range(0, fileCnt):
            filepath = (path+"test_"+randomFilename()+extn)
            filesize = get_file_size()
            sha_256 = utility.get_sha256(filepath,filesize)
            scan_entries.append(filepath+"|"+sha_256+"|"+get_signer()+"|"+str(filesize)+"|1")
       #print(path.join(randomFilename()))


def create_scanentries():
    scan_entries=[]
    spl_path=""
    for path in name.paths:
        if path.find("\\windows\\") > 0:
            createFiles(path, 200, scan_entries)

        if path.endswith("\\System32\\"):
            createFiles(path, 3000, scan_entries)

        if path.find("WinSxS") >= 0:
            for winsxsf in name.winsxs:
                spl_path = path+"\\"+winsxsf+"\\"
                createFiles(spl_path, 50, scan_entries)

        createFiles(path, 50, scan_entries)

    return scan_entries


def create_scanhashinfo(scan_file_loc):
    if os.path.isdir(scan_file_loc):
        scan_file_loc=scan_file_loc+"\\systemhashinfo.txt"
    with open(scan_file_loc, 'w') as h_scan_entry:
        h_scan_entry.write(";K7FileHashRecordType1\n")
        h_scan_entry.write(";FilePath|FileHash|FileSigner|FileSize|FileStatus\n")
        for entry in create_scanentries():
            h_scan_entry.write(entry+"\n")


def compress_file(root_dir, scan_arch_file):
    arch_file_name = scan_arch_file + ".zip"
    zip_file_path = root_dir + "\\" + arch_file_name

    if os.path.isdir(root_dir):
        scan_file_loc=root_dir+"\\systemhashinfo.txt"


    #arch_file_name = scan_arch_file+".zip"
    scn_hash_info_filename = scan_file_loc.split("\\")


    scn_zip = zipfile.ZipFile(zip_file_path,'w', zipfile.ZIP_DEFLATED)
    scn_zip.write(scan_file_loc, scn_hash_info_filename[len(scn_hash_info_filename)-1])
    scn_zip.close()
    zip_file_path_sha256 = root_dir+"\\"+str(utility.get_sha256_file(zip_file_path))+".zip"
    os.rename(zip_file_path,
              zip_file_path_sha256)
    print(zip_file_path_sha256)
    return zip_file_path_sha256


#scan_file_loc = os.environ['TEMP']+"\\systemhashinfo.txt"
#scan_arch_file = os.environ['TEMP']+"\\"
#create_scanhashinfo(scan_file_loc)
#compress_file(scan_file_loc, scan_arch_file)

