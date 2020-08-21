# Blackpearl Link Creator
Easy script to generate multiple links with <a href="https://github.com/rclone/rclone" tarbet="blank">rclone</a>.<br>
With this script you can generate download links for each file inside a folder, if you don't have the permissions to share a folder.<br>
You could also create multiple download links of folders with this script.

# How to Setup

- Download and Install <a href="https://github.com/rclone/rclone" tarbet="blank">rclone</a>

- Dowload and Install <a href="https://www.python.org/downloads/" tarbet="blank">Python</a>

- The Python Script.

If you didnt add rclone to your Systemvariables you need to place the Script inside the folder of rclone.

# Usage GUI
1. Open main.py<br>
<img src="https://i.ibb.co/cFrZ9nh/clean.png" alt="clean" border="0">
2. Enter (1) the rclone path of the files you want to share.
3. Check the Box (2) if you wanna add the hidereact and downcloud tag for your link.
4. Dont check the Box (2) if you dont want to add the hideract and downcloud tag for your link.
5. Click on Submit, wait a little bit and let the magic happen

# Result
- Hidereact enabled (Dont mention the empty downcloud tag. Its because of a folder thats not shareable)
<img src="https://i.ibb.co/C2nHJKh/hidereact-enabled.png" alt="hideract_enabled" border="0"><br><br>
If you enabled the check box, you can now easily copy & paste the result into your post!

- Hidereact disabled<br>
<img src="https://i.ibb.co/3cpmfvh/hidereact-disabled.png" alt="hideract_disabled" border="0"><br><br>

# Usage CLI
Version without hidereact:
```
python cli_clean.py remote:path
```

Version with hidereact:
```
python cli_hidereact.py remote:path
```
