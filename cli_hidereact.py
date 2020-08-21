import sys
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor


def RcloneLink(path):
    # Runs command "rclone link source:path"
    link = subprocess.run([
        "rclone",
        "link",
        path],
        encoding='utf-8',
        stdout=subprocess.PIPE)
    return link.stdout


def RcloneList(path):
    # Runs command "rclone lsf source:path"
    filelist = subprocess.run([
        "rclone",
        "lsf",
        path],
        encoding='utf-8',
        stdout=subprocess.PIPE)
    return filelist.stdout.strip().split("\n")


# Grabs Path From System Arugment (Console Input)
path = " ".join(sys.argv[1:])
# Runs RcloneList w/ System Argument to grab all file names
files = RcloneList(path)

# Add System Argument to beginning of every file name grabbed from RcloneList(path)
filesPath = [os.path.join(path, fl) for fl in files]

# Counter to list each iteration of variable "files" which is the file names
count = 0
# makes ThreadPoolExecutor() run when we say executor
with ThreadPoolExecutor() as executor:
    # link in ThreadPoolExecutor().map() This creates a queue to push the strings from filesPath to Def RcloneLink
    for result in executor.map(RcloneLink, filesPath):
        # use Count to grab each file name that is for each link print current iteration in list
        print(files[count])
        count += 1
        # Print Link
        print("[Hidereact=1,2,3,4,5,6][Downcloud]" + result + "[/downcloud][/hidereact]")
