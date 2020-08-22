###############################
###      Author: Shix       ###
###      Modder: Cocee      ###
###      Modder: Bilibox    ###
###      Version: 1.0.0     ###
###############################

from tkinter import *
import os
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor

font = "BlinkMacSystemFont"


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        master.title("Create Multiple File links - v1.0.0")
        self.init_window()

    # Creation of init_window
    def init_window(self):

        # Start process of creating links
        def write():

            path = rclone_entry.get()

            # Ensure we have an actual path!
            if path == "":
                rclone_text.delete(1.0, 'end')
                rclone_text.insert(INSERT, 'No Path Entered!')
                return

            clear()

            rclone_text.insert(INSERT, 'Grabbing Links For "' + path + '"\n\n')

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

            files = RcloneList(path)
            if len(files) == 0:
                rclone_text.insert(INSERT, "No Files Found!")
                return
            filesPath = [os.path.join(path, fl) for fl in files]
            count = 0

            with ThreadPoolExecutor() as executor:
                for result in executor.map(RcloneLink, filesPath):
                    c = files[count][:-4] + "\n"
                    p = result
                    count += 1

                    if hide_checkValue.get() == 1:
                        if count < 2:
                            rclone_text.insert(
                                INSERT, '[hidereact=1,2,3,4,5,6,7,8]\n')

                        rclone_text.insert(INSERT, c)

                        rclone_text.insert(
                            INSERT, "[downcloud]" +
                            p.replace('\n', '') + "[/downcloud]\n"
                            + "\n")

                        if len(filesPath) == count:
                            rclone_text.insert(INSERT, '[/hidereact]')
                    else:
                        print(c)
                        rclone_text.insert(INSERT, c)
                        rclone_text.insert(INSERT, p + '\n')

        # Clear rclone_text
        def clear():
            rclone_entry.delete(0, 'end')
            rclone_text.delete(1.0, 'end')

        # GUI
        rclone_lable = Label(self, text="Rclone path", font=(font, 13))
        rclone_lable.grid(column=0, row=1)

        rclone_entry = StringVar()
        rclone_entry = Entry(self, width=int(
            int(width)*0.13), borderwidth=2, font=(font, 10))
        rclone_entry.grid(column=0, row=2, pady=10)
        rclone_entry.focus_set()

        hide_checkValue = IntVar()
        hide_check = Checkbutton(
            self, text="Enable Hidereact", variable=hide_checkValue)
        hide_check.grid(column=0, row=3)

        rclone_text = Text(self, height=textHeight,
                           width=int(int(width)*0.13), borderwidth=2,
                           font=(font, 10))
        rclone_text.grid(column=0, row=4, pady=10)

        buttonWidth = int(int(width)*0.03)

        button_frame = Frame(root)
        button_frame.pack(fill=X, side=BOTTOM)

        rclone_button = Button(button_frame, text="Submit",
                               bg="green", width=buttonWidth, command=write)
        clear_button = Button(button_frame, text="Clear",
                              bg="green", width=buttonWidth, command=clear)

        button_frame.columnconfigure(index=0, weight=1)
        button_frame.columnconfigure(index=1, weight=1)

        rclone_button.grid(row=0, column=1, sticky=W+E)
        clear_button.grid(row=0, column=0, sticky=W+E)


if __name__ == "__main__":
    root = Tk()
    screen_width = root.winfo_screenwidth() * 0.20
    screen_height = root.winfo_screenheight() * 0.25
    width = re.sub(r'\..', '', str(screen_width))
    height = re.sub(r'\..', '', str(screen_height))
    if root.winfo_screenwidth() > 2000:
        textHeight = int(int(height)*0.04)
    elif root.winfo_screenwidth() > 1400:
        textHeight = int(int(height)*0.033)
    elif root.winfo_screenwidth() > 1000:
        textHeight = int(int(height)*0.02)
    root.geometry(width + "x" + height)
    Window(root).pack()
    root.mainloop()
