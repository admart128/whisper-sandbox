import whisper
import tkinter as tk
from tkinter import filedialog
from googletrans import Translator
import yt_dlp
import tempfile
import os

# Function to download audio from YouTube
def download_audio_from_youtube(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': tempfile.gettempdir() + '/%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        temp_file = ydl.prepare_filename(info).replace('.webm', '.mp3')
        return temp_file

# Initialize the tkinter window
window = tk.Tk()
window.title("whisper-sandbox")
window.geometry("750x750")

translator = Translator()

# Function to select a file and transcribe it
def select_file():
    file_path = filedialog.askopenfilename(initialdir="/", title="Select A File", filetypes=(("mp3 files", "*.mp3"),))
    model = whisper.load_model("medium")
    result = model.transcribe(file_path)
    text = result["text"]
    output_text.delete('1.0', tk.END)
    output_text.insert(tk.END, text)

# Function to process a YouTube link and transcribe the audio
def process_youtube_link():
    url = youtube_url_entry.get()
    if url:
        file_path = download_audio_from_youtube(url)
        model = whisper.load_model("medium")
        result = model.transcribe(file_path)
        text = result["text"]
        output_text.delete('1.0', tk.END)
        output_text.insert(tk.END, text)

# Function to translate the selected text
def translate_text(event):
    selected_text = output_text.selection_get()
    if selected_text:
        translated = translator.translate(selected_text, dest='en')
        translation_text.delete('1.0', tk.END)
        translation_text.insert(tk.END, translated.text)

# Create and configure tkinter widgets
select_file_button = tk.Button(window, text="Select MP3 file", command=select_file)
select_file_button.pack()

youtube_url_label = tk.Label(window, text="Enter YouTube video URL")
youtube_url_label.pack()

youtube_url_entry = tk.Entry(window, width=80)
youtube_url_entry.pack()

youtube_button = tk.Button(window, text="Download and Transcribe YouTube Audio", command=process_youtube_link)
youtube_button.pack()

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