import whisper
import tkinter as tk
import tkinter.font as tkFont
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
    if output_text.tag_ranges("sel"):
        selected_text = output_text.selection_get()
        if selected_text:
            translated = translator.translate(selected_text, dest='en')
            translation_text.delete('1.0', tk.END)
            translation_text.insert(tk.END, translated.text)

# Function to handle text size changes
def resize_text(event):
    font_obj = tkFont.Font(font=output_text.cget('font'))
    font_size = font_obj['size']

    if event.state == 0x4:
        # Check if Ctrl key is being held down
        if event.keysym == 'plus':
            # Increase text size
            font_obj.configure(size=font_size+1)
            output_text.configure(font=font_obj)
            translation_text.configure(font=font_obj)
        elif event.keysym == 'minus':
            # Decrease text size
            if font_size > 1:
                font_obj.configure(size=font_size-1)
                output_text.configure(font=font_obj)
                translation_text.configure(font=font_obj)
    elif event.num == 4:
        # Mouse wheel up
        font_obj.configure(size=font_size+1)
        output_text.configure(font=font_obj)
        translation_text.configure(font=font_obj)
    elif event.num == 5:
        # Mouse wheel down
        if font_size > 1:
            font_obj.configure(size=font_size-1)
            output_text.configure(font=font_obj)
            translation_text.configure(font=font_obj)

# create and configure widgets for the first grid
select_file_button = tk.Button(window, text="Select MP3 file", command=select_file)
select_file_button.grid(row=0, column=0, sticky="n")

youtube_url_label = tk.Label(window, text="Enter YouTube video URL")
youtube_url_label.grid(row=1, column=0, sticky="n")

youtube_url_entry = tk.Entry(window, width=80)
youtube_url_entry.grid(row=2, column=0, sticky="n")

youtube_button = tk.Button(window, text="Transcribe YouTube Audio", command=process_youtube_link)
youtube_button.grid(row=3, column=0, sticky="n")

# create a frame for the second grid
frame = tk.Frame(window)
frame.grid(row=4, column=0, columnspan=2, pady=10)

transcription_label = tk.Label(frame, text="Transcript")
transcription_label.grid(row=0, column=0, sticky="n", pady=5)

output_text = tk.Text(frame, height=20, width=30)
output_text.grid(row=1, column=0, sticky="w")
output_text.bind("<<Selection>>", translate_text)
output_text.bind("<Control-plus>", resize_text)
output_text.bind("<Control-minus>", resize_text)
output_text.bind("<Button-4>", resize_text)
output_text.bind("<Button-5>", resize_text)

translation_label = tk.Label(frame, text="Translation")
translation_label.grid(row=0, column=1, sticky="n", pady=5)

translation_text = tk.Text(frame, height=20, width=30)
translation_text.grid(row=1, column=1, sticky="w")
translation_text.bind("<<Selection>>", translate_text)
translation_text.bind("<Control-plus>", resize_text)
translation_text.bind("<Control-minus>", resize_text)
translation_text.bind("<Button-4>", resize_text)
translation_text.bind("<Button-5>", resize_text)

# set the height of each row to 0 in the first grid
for i in range(4):
    window.grid_rowconfigure(i, minsize=1)

# set the width of the columns in the first grid
window.columnconfigure(0, weight=1)

# set the height of each row to 0 in the second grid
for i in range(2):
    frame.grid_rowconfigure(i, minsize=1)

# set the width of the columns in the second grid
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)

# start the main event loop
window.mainloop()