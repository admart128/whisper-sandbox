import whisper
import tkinter as tk
from tkinter import filedialog
from googletrans import Translator
from pytube import YouTube
import tempfile
import os

def download_audio_from_youtube(url):
    video = YouTube(url)
    audio_stream = video.streams.filter(only_audio=True).first()
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, f"{video.title}.mp3")
    audio_stream.download(output_path=temp_dir, filename=video.title)
    return temp_file

window = tk.Tk()
window.title("whisper-sandbox")
window.geometry("750x750")

filename = ""

translator = Translator()

def select_file():

    
    file_path = filedialog.askopenfilename(
        initialdir="/", title="Select A File", filetypes=(("mp3 files", "*.mp3"),))
    
    
    #url = input("Enter the YouTube video URL: ")
    #file_path = download_audio_from_youtube(url)
   

    file_path = download_audio_from_youtube(url)
    model = whisper.load_model("medium")
    result = model.transcribe(file_path)
    text = result["text"]
    output_text.delete('1.0', tk.END)
    output_text.insert(tk.END, text)

    def process_youtube_link():
        url = youtube_link_entry.get()
        if not url:
            return

    model = whisper.load_model("medium")
    result = model.transcribe(file_path)
    text = result["text"]
    output_text.delete('1.0', tk.END)
    output_text.insert(tk.END, text)

def translate_text(event):
    selected_text = output_text.selection_get()
    if selected_text:
            translated = translator.translate(selected_text, dest='en')
            translation_text.delete('1.0', tk.END)
            translation_text.insert(tk.END, translated.text)

youtube_link_label = tk.Label(window, text="Enter YouTube Video URL:")
youtube_link_label.pack()

youtube_link_entry = tk.Entry(window, width=80)
youtube_link_entry.pack()

youtube_button = tk.Button(window, text="Download and Transcribe YouTube Audio", command=process_youtube_link)
youtube_button.pack()


button = tk.Button(window, text="Select MP3 File", command=select_file)
button.pack()

transcription_label = tk.Label(window, text="Transcription")
transcription_label.pack()

output_text = tk.Text(window, height=30, width=80)
output_text.pack()
output_text.bind("<<Selection>>", translate_text)

translation_label = tk.Label(window, text="Translation")
translation_label.pack()

translation_text = tk.Text(window, height=10, width=80)
translation_text.pack()

window.mainloop()