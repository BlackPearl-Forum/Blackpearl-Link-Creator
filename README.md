# BlackPearl Link Creator
Easy script to generate multiple links with <a href="https://github.com/rclone/rclone" target="blank">Rclone</a>.<br>
With this script you can generate download links for each file inside a folder and for every file in sub folders, if you don't have the permissions to share a folder.<br>
You could also create multiple download links of folders with this script.

# How to Setup

- Download and Install <a href="https://github.com/rclone/rclone" target="blank">Rclone</a>

- Download and Install <a href="https://www.python.org/downloads/" target="blank">Python 3.6+</a>

- Download links.py

If you didn't add Rclone to your SystemVariables you need to place the Script inside the folder of Rclone.

# Arguments
'--remote' or '-r'<br>
Set The Rclone Remote Path Ex: Gdrive:folder/path <br>

'--hidereact' or '-hr'<br> 
Use Hidereact BBCode With Link Output <br>

'--downcloud' or '-dc'<br>
Use Downcloud BBCode With Link Output <br>

'--nolinks' or '-nl'<br>
Print Out File Names Only (In Development)') <br>

'--gui' or '-g'<br>
Launch Script As A Gui <br>

'--update' or '-u'<br>
Update Script To The Newest Version <br>

# Usage GUI
1. Run Script with --gui argument. `links.py --gui` OR rename links.py to links.pyw Open it.<br><img src="https://i.ibb.co/cFrZ9nh/clean.png" alt="clean" border="0">
2. Enter (1) the Rclone path of the files you want to share.
3. Check the Box (2) if you wanna add the hidereact and downcloud tag for your link.
4. Don't check the Box (2) if you don't want to add the hidereact and downcloud tag for your link.
5. Click on Submit, wait a little bit and let the magic happen.

# Result
- Hidereact enabled (Don't mention the empty downcloud tag. Its because of a folder thats not shareable)
<img src="https://i.ibb.co/C2nHJKh/hidereact-enabled.png" alt="hidereact_enabled" border="0"><br><br>
If you enabled the check box, you can now easily copy & paste the result into your post!

- Hidereact disabled<br>
<img src="https://i.ibb.co/3cpmfvh/hidereact-disabled.png" alt="hidereact_disabled" border="0"><br><br>

# Usage CLI
```
usage: links.py [-h] [--remote REMOTE] [--hidereact] [--downcloud] [--nolinks] [--gui] [--update]

Get them infos

optional arguments:
  -h, --help            show this help message and exit
  --remote REMOTE, -r REMOTE
                        Set The Rclone Remote Path Ex: Gdrive:folder/path
  --hidereact, -hr      Use Hidereact BBCode With Link Output
  --downcloud, -dc      Use Downcloud BBCode With Link Output
  --nolinks, -nl        Print Out File Names Only (In Development)
  --gui, -g             Launch Script As A Gui
  --update, -u          Update Script To The Newest Version
```
Example with Hidereact and Downcloud:
```
links.py -r Gdrive:folder/path -hr -dc
[Hidereact=1,2,3,4,5,6,7,8]
File1
[Downcloud]link1[/downcloud]
File2
[Downcloud]link2[/downcloud]
[/hidereact]
```
Example with only Hidereact:
```
links.py -r Gdrive:folder/path -hr
[Hidereact=1,2,3,4,5,6,7,8]
File1
link1

File2
link2
[/hidereact]
```
