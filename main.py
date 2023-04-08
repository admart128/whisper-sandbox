import whisper
import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog
from googletrans import Translator
from gtts import gTTS
import yt_dlp
import tempfile
import os
import pygame
import threading
import time

model = whisper.load_model("medium")

window = tk.Tk()
window.title("🐦 wordbird")
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry("%dx%d+%d+0" % (screen_width // 2, screen_height, 0))

image = tk.PhotoImage(file="images/birb.png")

context_menu = None

translator = Translator()
selected_input_language = tk.StringVar(value="English")
selected_output_language = tk.StringVar(value="English")
input_language_code = tk.StringVar(value="en")
output_language_code = tk.StringVar(value="en")


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


def select_file():
    file_path = filedialog.askopenfilename(
        initialdir="/", title="Select A File", filetypes=(("mp3 files", "*.mp3"),))
    result = model.transcribe(file_path)  # Reuse the loaded model
    text = result["text"]
    transcript_text.delete('1.0', tk.END)
    transcript_text.insert(tk.END, text)


def process_youtube_link():
    url = youtube_url_entry.get()
    if url:
        file_path = download_audio_from_youtube(url)
        result = model.transcribe(file_path)
        text = result["text"]
        transcript_text.delete('1.0', tk.END)
        transcript_text.insert(tk.END, text)


stop_flag = False
lang_code = "en"


def play_text(text, slow=False, language_code="en"):
    global stop_flag
    print("Playing Text:", text)
    print("Language Code:", lang_code)
    tts = gTTS(text=text, lang=language_code, slow=slow)
    tts.save("temp_speech.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("temp_speech.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        if stop_flag:
            pygame.mixer.music.stop()
            stop_flag = False
            break
        time.sleep(0.1)
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    os.remove("temp_speech.mp3")


# def highlight_selection(event):
  #  event.widget.tag_configure(tk.SEL, background="lightblue")
   # event.widget.tag_raise(tk.SEL)
def get_highlight_position(widget):
    if widget.tag_ranges("sel"):
        x, y, _, _ = widget.bbox(tk.SEL_FIRST)
        x_offset = widget.winfo_rootx()
        y_offset = widget.winfo_rooty()
        return x_offset + x, y_offset + y
    else:
        return None

def cut_text(widget):
    if widget.tag_ranges(tk.SEL):
        widget.event_generate("<<Cut>>")

def copy_text(widget):
    if widget.tag_ranges(tk.SEL):
        widget.event_generate("<<Copy>>")

def paste_text(widget):
    if widget.tag_ranges(tk.SEL):
        widget.delete(tk.SEL_FIRST, tk.SEL_LAST)
    widget.event_generate("<<Paste>>")

def highlight_text(event):
    global context_menu

    if event.widget.tag_ranges("sel"):
        selected_text = event.widget.selection_get()

        if event.widget == transcript_text:
            lang_code = input_language_code.get()
        elif event.widget == translation_text:
            lang_code = output_language_code.get()

    if event.num == 3:

        if context_menu:
            context_menu.unpost()
            context_menu = None

        context_menu = tk.Menu(event.widget, tearoff=0)

        cut_state = tk.DISABLED
        copy_state = tk.DISABLED
        translate_state = tk.DISABLED
        tts_state = tk.DISABLED
        tts_slow_state = tk.DISABLED
        cover_state = tk.DISABLED
        reveal_state = tk.DISABLED

        if event.widget.tag_ranges("sel"):
            cut_state = tk.NORMAL
            copy_state = tk.NORMAL
            translate_state = tk.NORMAL
            tts_state = tk.NORMAL
            tts_slow_state = tk.NORMAL
            cover_state = tk.NORMAL
            reveal_state = tk.NORMAL

        context_menu.add_command(label="Cut", command=lambda: cut_text(event.widget), state=cut_state)
        context_menu.add_command(label="Copy", command=lambda: copy_text(event.widget), state=copy_state)
        context_menu.add_command(label="Paste", command=lambda: paste_text(event.widget))
        context_menu.add_separator()

        context_menu.add_command(label="Translate", command=translate_text, state=translate_state)
        context_menu.add_command(label="Text to Speech", command=lambda: threading.Thread(
            target=play_text, args=(selected_text,), kwargs={'slow': False, 'language_code': lang_code}).start(),
            state=tts_state)
        context_menu.add_command(label="Text to Speech (Slow)", command=lambda: threading.Thread(
            target=play_text, args=(selected_text,), kwargs={'slow': True, 'language_code': lang_code}).start(),
            state=tts_slow_state)
        context_menu.add_command(label="Abort Text to Speech", command=lambda: stop_tts())
        context_menu.add_command(label="Cover Text", command=lambda: cover_text(event), state=cover_state)
        context_menu.add_command(label="Reveal Text", command=lambda: reveal_text(event), state=reveal_state)

        context_menu.post(event.x_root, event.y_root)



            #highlight_position = get_highlight_position(event.widget)
            #if highlight_position:
                #context_menu.post(*highlight_position)



def translate_text():
    selected_text = transcript_text.selection_get()
    print("Selected Text:", selected_text)
    translated = translator.translate(
        selected_text, dest=output_language_code.get())
    print("Translation:", translated.text)
    translation_text.delete('1.0', tk.END)
    translation_text.insert(tk.END, translated.text)


def cover_text(event):
    widget = event.widget
    if widget.tag_ranges("sel"):
        widget.tag_configure(
            "covered", background="black", foreground="black")
        widget.tag_add("covered", widget.index(
            tk.SEL_FIRST), widget.index(tk.SEL_LAST))


def reveal_text(event):
    widget = event.widget
    if widget.tag_ranges("sel"):
        widget.tag_remove("covered", "1.0", tk.END)


def stop_tts():
    global stop_flag
    stop_flag = True
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    stop_flag = False


def close_context_menu(event):
    transcript_text.delete("menu")
    translation_text.delete("menu")


def open_context_menu(event):
    widget = event.widget
    if isinstance(widget, tk.Text):
        if widget.tag_ranges(tk.SEL):
            highlight_text(event)
            widget.after(100, close_context_menu, event)
        else:
            widget.after(100, close_context_menu, event)


def resize_text(event):
    font_obj = tkFont.Font(font=transcript_text.cget('font'))
    font_size = font_obj['size']

    if event.state == 0x4:
        if event.keysym == 'plus':
            font_obj.configure(size=font_size+1)
            transcript_text.configure(font=font_obj)
            translation_text.configure(font=font_obj)
        elif event.keysym == 'minus':
            if font_size > 1:
                font_obj.configure(size=font_size-1)
                transcript_text.configure(font=font_obj)
                translation_text.configure(font=font_obj)
    elif event.num == 4:
        font_obj.configure(size=font_size+1)
        transcript_text.configure(font=font_obj)
        translation_text.configure(font=font_obj)
    elif event.num == 5:
        if font_size > 1:
            font_obj.configure(size=font_size-1)
            transcript_text.configure(font=font_obj)
            translation_text.configure(font=font_obj)


select_file_button = tk.Button(
    window, text="Select MP3 file", command=select_file)
select_file_button.grid(row=0, column=0, sticky="n")

youtube_url_label = tk.Label(window, text="Enter YouTube video URL")
youtube_url_label.grid(row=1, column=0, sticky="n")

youtube_url_entry = tk.Entry(window, width=80)
youtube_url_entry.grid(row=2, column=0, sticky="n")

youtube_button = tk.Button(
    window, text="Transcribe YouTube Audio", command=process_youtube_link)
youtube_button.grid(row=3, column=0, sticky="n")

abort_button = tk.Button(window, text="Abort Text to Speech", command=stop_tts)
abort_button.grid(row=4, column=0, sticky="n")

frame = tk.Frame(window)
frame.grid(row=5, column=0, columnspan=2)

transcript_label = tk.Label(frame, text="Transcript")
transcript_label.grid(row=0, column=0, sticky="n")

transcript_text = tk.Text(frame, height=20, width=30)
transcript_text.grid(row=1, column=0, sticky="n")
transcript_text.bind("<Button-3>", highlight_text)
# transcript_text.bind("<<Selection>>", highlight_text)
transcript_text.bind("<Button-4>", resize_text)
transcript_text.bind("<Button-5>", resize_text)

translation_label = tk.Label(frame, text="Translation")
translation_label.grid(row=0, column=1, sticky="n")

translation_text = tk.Text(frame, height=20, width=30)
translation_text.grid(row=1, column=1, sticky="n")
translation_text.bind("<Button-3>", highlight_text)
# translation_text.bind("<<Selection>>", highlight_text)
translation_text.bind("<Button-4>", resize_text)
translation_text.bind("<Button-5>", resize_text)

window.bind("<Button-3>", close_context_menu)

for i in range(4):
    window.grid_rowconfigure(i, minsize=1)
window.columnconfigure(0, weight=1)
for i in range(2):
    frame.grid_rowconfigure(i, minsize=1)
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)

# selected_language = tk.StringVar(value="English")


class CustomOptionMenu(tk.OptionMenu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)

    def _on_focus_in(self, event):
        self.previous_focus = self.focus_get()

    def _on_focus_out(self, event):
        if self.previous_focus:
            self.previous_focus.focus_set()

birb_label = tk.Label(window, image=image)
birb_label.grid(row=0, column=0, sticky="w", padx=10)

input_language_label = tk.Label(window, text="Input Language")
input_language_label.grid(row=0, column=1, sticky="w", padx=10)

input_language_options = ["English", "한국어", "日本語"]
# input_language_menu = tk.OptionMenu(
#    window, selected_input_language, *input_language_options)
# input_language_menu.grid(row=1, column=1, sticky="w", padx=10)
input_language_menu = CustomOptionMenu(
    window, selected_input_language, *input_language_options)
input_language_menu.grid(row=1, column=1, sticky="w", padx=10)

output_language_label = tk.Label(window, text="Output Language")
output_language_label.grid(row=2, column=1, sticky="w", padx=10)


def save_and_restore_selection(widget, command):
    selection_exists = bool(widget.tag_ranges("sel"))
    if selection_exists:
        start_index = widget.index(tk.SEL_FIRST)
        end_index = widget.index(tk.SEL_LAST)
    command()
    if selection_exists:
        widget.tag_add("sel", start_index, end_index)


output_language_options = ["English", "한국어", "日本語"]
# output_language_menu = tk.OptionMenu(
#    window, selected_output_language, *output_language_options)
# output_language_menu.grid(row=3, column=1, sticky="w", padx=10)

output_language_menu = CustomOptionMenu(
    window, selected_output_language, *output_language_options)
output_language_menu.grid(row=3, column=1, sticky="w", padx=10)


def select_input_language(*args):
    global input_language_code
    if selected_input_language.get() == "English":
        input_language_code.set("en")
    elif selected_input_language.get() == "한국어":
        input_language_code.set("ko")
    elif selected_input_language.get() == "日本語":
        input_language_code.set("ja")


def select_output_language(*args):
    global output_language_code
    if selected_output_language.get() == "English":
        output_language_code.set("en")
    elif selected_output_language.get() == "한국어":
        output_language_code.set("ko")
    elif selected_output_language.get() == "日本語":
        output_language_code.set("ja")


input_language_menu = tk.OptionMenu(
    window, selected_input_language, *input_language_options)
input_language_menu.grid(row=1, column=1, sticky="w", padx=10)

output_language_menu = tk.OptionMenu(
    window, selected_output_language, *output_language_options)
output_language_menu.grid(row=3, column=1, sticky="w", padx=10)

selected_input_language.trace("w", select_input_language)
selected_output_language.trace("w", select_output_language)


def close_context_menu(event):
    transcript_text.delete("menu")
    translation_text.delete("menu")


def close_context_menu_on_click(event):
    global context_menu
    if context_menu:
        context_menu.unpost()
        context_menu = None


window.bind('<Button-1>', close_context_menu_on_click)
frame.bind('<Button-1>', close_context_menu_on_click)

window.mainloop()