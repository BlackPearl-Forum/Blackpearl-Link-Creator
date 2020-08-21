import sys
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor


def RcloneLink(path):
    link = subprocess.run([
        "rclone",
        "link",
        path],
        encoding='utf-8',
        stdout=subprocess.PIPE)
    return link.stdout


def RcloneList(path):
    filelist = subprocess.run([
        "rclone",
        "lsf",
        path],
        encoding='utf-8',
        stdout=subprocess.PIPE)
    return filelist.stdout.strip().split("\n")


path = " ".join(sys.argv[1:])
files = RcloneList(path)
links = []

filesPath = [os.path.join(path, fl) for fl in files]
count = 0
with ThreadPoolExecutor() as executor:
    for result in executor.map(RcloneLink, filesPath):
        print(files[count])
        count += 1
        print(result)
