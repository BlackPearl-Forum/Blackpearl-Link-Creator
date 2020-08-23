###############################
###      Author: Bilibox    ###
###      Modder: Cocee      ###
###      Version: 1.0.2     ###
###############################

import sys
import os
import subprocess
import argparse
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


# Enable arg parser for bools and remote
parser = argparse.ArgumentParser(description='Get them infos')

parser.add_argument('--remote', '-r', type=str, default=None,
                    help='Set the Rclone Remote Path Ex: Gdrive:folder/path')
parser.add_argument('--hidereact', '-hr', default=False, action='store_true',
                    help='Use Hidereact BBCode with link output')
parser.add_argument('--downcloud', '-dc', default=False, action='store_true',
                    help='Use Downcloud BBCode with link output')

args = parser.parse_args()

# Check Remote string
path = input(
    "Input your Rclone Remote: ") if args.remote is None else args.remote

# Runs RcloneList w/ path to grab all file names
files = RcloneList(path)

# Add arg.remote to beginning of every file name grabbed from RcloneList(path)
filesPath = [os.path.join(path, fl) for fl in files]

# Counter to list each iteration of variable "files" which is the file names
count = 0
hidebbcode = ["[Hidereact=1,2,3,4,5,6,7,8]",
              "[/hidereact]"] if args.hidereact is True else ["", ""]
downcloudBBcode = ["[Downcloud]",
                   "[/downcloud]"] if args.downcloud is True else ["", ""]
# makes ThreadPoolExecutor() run when we say executor
with ThreadPoolExecutor() as executor:
    # link in ThreadPoolExecutor().map() This creates a queue to push the
    # strings from filesPath to Def RcloneLink
    for result in executor.map(RcloneLink, filesPath):
        # use Count to grab each file name that is for each link print current
        # iteration in list
        print(files[count])
        count += 1
        # Print Link
        print(hidebbcode[0] + downcloudBBcode[0] +
              result + downcloudBBcode[1] + hidebbcode[1])
