from tkinter import *
from tkinter import simpledialog
import pytube
import moviepy.editor as mp
import os
import win32console,win32gui
import tkinter.messagebox

def hide():
    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window,0)
    return True

def view():
    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window,1)
    return True

def download():
	video_url = url.get()
	try:
		name = filename()
		if not name:
			return
		for i in name:
			if i == ".":
				tkinter.messagebox.showerror(title="Error", message="Write the filename without the extension")
				return
		name = name + ".mp4"


		youtube = pytube.YouTube(video_url)
		video = youtube.streams.filter(adaptive=True).first().download()
		os.rename(video, "video.mp4")
		song = youtube.streams.filter(only_audio=True).first().download()
		os.rename(song, "song.mp3")
		
		clip = mp.VideoFileClip("video.mp4")
		audio = mp.AudioFileClip("song.mp3")
		
		final_clip = clip.set_audio(audio)
		final_clip.write_videofile(name)
		os.remove("video.mp4")
		os.remove("song.mp3")

		tkinter.messagebox.showinfo(title="Success", message="Download complete")
		notif.config(fg="green",text="Download complete")

	except Exception as e:
		tkinter.messagebox.showerror(title="Error", message=f"Video could not be downloaded ({e})")
		notif.config(fg="red",text="Video could not be downloaded")

def filename():
	name = simpledialog.askstring("Filename", "Please enter the filename")
	return name

hide()
window = Tk()
window.title("YVD")

Label(window, text="YouTube Video Downloader", fg="#f00", font=("Calibri", 15)).grid(sticky=N, padx=100,row=0)
Label(window, text="Please enter your video link below : ", font=("Calibri", 12)).grid(sticky=N, pady=15,row=1)
notif = Label(window, font=("Calibri", 12))
notif.grid(sticky=N, pady=1, row=4)

url = StringVar()

Entry(window, width=50, textvariable=url).grid(sticky=N, row=2)

Button(window, width=10, text="Download", font=("Calibri", 12), command=download, fg="#fff", background="#c00").grid(sticky=N, row=3, pady=15)

window.iconbitmap("image/icon.ico")
window.mainloop()

view()
