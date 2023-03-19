import whisper
import tkinter as tk
from tkinter import filedialog
from googletrans import Translator
import yt_dlp
import tempfile

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

window = tk.Tk()
window.title("whisper-sandbox")
window.geometry("750x750")

translator = Translator()

def process_youtube_link():
    url = youtube_url_entry.get()
    if url:
        file_path = download_audio_from_youtube(url)
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