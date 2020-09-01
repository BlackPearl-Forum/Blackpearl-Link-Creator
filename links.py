try:
    import tkinter as tk
    from tkinter import scrolledtext
    import os
    import base64
    import sys
    import subprocess
    import argparse
    import pkg_resources
    from concurrent.futures import ThreadPoolExecutor
    from packaging import version
    import requests
    import lxml.html as ltml
except Exception as e:
    required = {'requests', 'lxml'}
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed
    if missing:
        python = sys.executable
        subprocess.check_call(
            [python, '-m', 'pip', 'install', *missing],
            stdout=subprocess.DEVNULL)


__version__ = '1.0.3'


class LinkChecker():
    def __init__(self):
        self._scriptFileName = os.path.basename(__file__)

    def RcloneLink(self, path):
        link = subprocess.run([
            "rclone",
            "link",
            path],
            encoding='utf-8',
            stderr=subprocess.DEVNULL,
            stdout=subprocess.PIPE)
        return link.stdout

    def RcloneList(self, path):
        stdOutput = subprocess.run([
            "rclone",
            "lsf",
            "-R",
            path],
            encoding='utf-8',
            stderr=subprocess.DEVNULL,
            stdout=subprocess.PIPE)
        filelist = stdOutput.stdout.strip().split("\n")
        filelist.sort()
        return filelist

    def Updater(self):
        print("Updating... Please wait!")
        try:
            updateURL = ('https://raw.githubusercontent.com/BlackPearl-Forum' +
                         '/Blackpearl-Link-Creator/master/links.py')
            latestFile = requests.get(updateURL)
            if latestFile.status_code == 200:
                with open(self._scriptFileName, 'wb') as script:
                    script.write(latestFile.content)
                sys.exit("Script has been updated.")
            else:
                sys.exit("Script NOT updated. Please manually update.")
        except Exception as e:
            sys.exit("Updater Failed: " + e)

    def UpdateCheck(self):
        uCheckURL = ("https://github.com/BlackPearl-Forum/" +
                     "Blackpearl-Link-Creator/releases/latest")
        req = requests.get(uCheckURL)
        tree = ltml.fromstring(req.content)
        latestVer = tree.find('.//span[@class="css-truncate-target"]').text
        if version.parse(latestVer) > version.parse(__version__):
            return True
        else:
            return False

    def ParseArgs(self):
        parser = argparse.ArgumentParser(description='Get them infos')
        parser.add_argument(
            '--remote', '-r', type=str, default=None,
            help='Set The Rclone Remote Path Ex: Gdrive:folder/path')
        parser.add_argument(
            '--hidereact', '-hr', default=False, action='store_true',
            help='Use Hidereact BBCode With Link Output')
        parser.add_argument(
            '--downcloud', '-dc', default=False, action='store_true',
            help='Use Downcloud BBCode With Link Output')
        parser.add_argument(
            '--nolinks', '-nl', default=False, action='store_true',
            help='Print Out File Names Only (In Development)')
        parser.add_argument(
            '--gui', '-g', default=False, action='store_true',
            help='Launch Script As A Gui')
        parser.add_argument(
            '--update', '-u', default=False, action='store_true',
            help='Update Script To The Newest Version')
        return parser.parse_args()

    def OutputList(self):
        path = input(
            "Input Your Rclone Remote: "
        ) if self.args.remote is None else self.args.remote

        files = self.RcloneList(path)

        if len(files) <= 1 and '' in files:
            sys.exit("There are no Files or the Remote is incorrect.")

        filesPath = [os.path.join(path, fl) for fl in files]

        count = 0

        hidebbcode = [
            "[Hidereact=1,2,3,4,5,6,7,8]",
            "[/Hidereact]"
        ] if self.args.hidereact is True else ["", ""]
        downcloudBBcode = [
            "[Downcloud]",
            "[/Downcloud]"
        ] if self.args.downcloud is True else ["", ""]
        arrLength = len(filesPath)
        with ThreadPoolExecutor() as executor:
            for result in executor.map(self.RcloneLink, filesPath):
                if count == 0:
                    print('\n' + hidebbcode[0] + '\n')
                print(os.path.splitext(files[count])[0])
                count += 1
                print(downcloudBBcode[0] +
                      result.replace('\n', '') + downcloudBBcode[1] + '\n')
                if arrLength == count:
                    print(hidebbcode[1])

    def Main(self):
        self.args = self.ParseArgs()
        if self.args.update:
            self.Updater()
        if self.args.gui or ".pyw" in self._scriptFileName:
            Gui().startGUI()
        else:
            updateBool = self.UpdateCheck()
            if updateBool:
                print("Update Avaliable!")
            self.OutputList()


class Gui():
    def __init__(self):
        self.masterWindow = tk.Tk()
        self.masterWindow.title("BlackPearl Link Creator " + __version__)

    def startGUI(self):
        optionsFrame = tk.Frame(self.masterWindow)
        optionsFrame.grid(row=0, column=0, sticky=tk.W+tk.E)

        self.masterWindow.columnconfigure(0, weight=1)
        self.masterWindow.rowconfigure(1, weight=1)

        rPathLabel = tk.Label(optionsFrame, text="Rclone Path")
        rPathLabel.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.rPathInput = tk.Entry(optionsFrame, borderwidth=2, width=25)
        self.rPathInput.grid(row=0, column=1, padx=5, pady=5)
        self.rPathInput.focus_set()

        self.hideValue = tk.IntVar()
        hideButton = tk.Checkbutton(
            optionsFrame, text="Enable Hidereact", var=self.hideValue)
        hideButton.grid(row=0, column=2)

        self.downValue = tk.IntVar()
        downButton = tk.Checkbutton(
            optionsFrame, text="Enable Downcloud", var=self.downValue)
        downButton.grid(row=1, column=2)

        group1 = tk.LabelFrame(
            self.masterWindow, text="Output", padx=5, pady=5)
        group1.grid(row=1, column=0, columnspan=3,
                    padx=5, pady=5, sticky=tk.E+tk.W+tk.N+tk.S)

        group1.rowconfigure(0, weight=1)
        group1.columnconfigure(0, weight=1)

        self.OutputBox = scrolledtext.ScrolledText(
            group1, width=20, height=5)
        self.OutputBox.grid(row=0, column=0, sticky=tk.E+tk.W+tk.N+tk.S)

        buttonsFrame = tk.Frame(self.masterWindow)
        buttonsFrame.grid(row=3, column=0, sticky=tk.W+tk.E+tk.S)

        runButton = tk.Button(
            buttonsFrame, text='Submit', bg="#4CAF50", command=self.Submit)
        runButton.grid(row=0, column=0, sticky=tk.E+tk.W)

        clrButton = tk.Button(
            buttonsFrame, text='Clear', bg="#f44336", command=self.Clear)
        clrButton.grid(row=0, column=1, sticky=tk.W+tk.E)

        buttonsFrame.columnconfigure(index=0, weight=1)
        buttonsFrame.columnconfigure(index=1, weight=1)
        buttonsFrame.rowconfigure(0, weight=1)

        iconDL = requests.get('https://blackpearl.biz/favicon.png').content
        b64_data = base64.encodebytes(iconDL)
        image = tk.PhotoImage(data=b64_data)
        self.masterWindow.call('wm', 'iconphoto', self.masterWindow._w, image)

        self.masterWindow.geometry("500x500")
        updateBool = LinkChecker().UpdateCheck()
        if updateBool:
            self.OutputBox.insert(tk.INSERT, 'Update Avaliable!')
        self.masterWindow.mainloop()

    def Clear(self):
        self.rPathInput.delete(0, 'end')
        self.OutputBox.delete(1.0, 'end')

    def Submit(self):
        path = self.rPathInput.get()
        if path == "":
            self.OutputBox.delete(1.0, 'end')
            self.OutputBox.insert(tk.INSERT, 'No Path Entered!')
            return

        self.OutputBox.insert(
            tk.INSERT, 'Grabbing Links For "' + path + '"\n\n')

        files = LinkChecker().RcloneList(path)
        if len(files) == 0:
            self.OutputBox.insert(tk.INSERT, "No Files Found!")
            return
        filesPath = [os.path.join(path, fl) for fl in files]
        count = 0

        hidebbcode = [
            "[Hidereact=1,2,3,4,5,6,7,8]",
            "[/hidereact]"
        ] if self.hideValue.get() == 1 else ["", ""]
        downcloudBBcode = [
            "[Downcloud]",
            "[/downcloud]"
        ] if self.downValue.get() == 1 else ["", ""]

        with ThreadPoolExecutor() as executor:
            for result in executor.map(LinkChecker().RcloneLink, filesPath):
                fileName = os.path.splitext(files[count])[0] + "\n"
                fileLink = result
                count += 1
                if count == 1:
                    self.OutputBox.insert(tk.INSERT, hidebbcode[0] + '\n')
                self.OutputBox.insert(tk.INSERT, fileName)
                self.OutputBox.insert(
                    tk.INSERT, downcloudBBcode[0] +
                    fileLink.replace('\n', '') + downcloudBBcode[1] + '\n\n')
                if len(filesPath) == count:
                    self.OutputBox.insert(tk.INSERT, hidebbcode[1])


if __name__ == "__main__":
    LinkChecker().Main()
