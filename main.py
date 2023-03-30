import whisper
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.core.window import Window
from googletrans import Translator
from gtts import gTTS
from langdetect import detect
import yt_dlp
import tempfile
import os
import pygame
import threading
import time

from kivy.config import Config
from kivy.core.text import LabelBase

fonts_by_language = {
    'default': 'fonts/NotoSans-Regular.ttf',
    'ja': 'fonts/NotoSansJP-Regular.otf',
    'ko': 'fonts/NotoSansKR-Regular.otf',
    # Add more language codes and fonts if needed
}

def load_font_for_language(language_code):
    font_path = fonts_by_language.get(language_code, fonts_by_language['default'])
    return font_path

# Register the default font
LabelBase.register(name='default_font', fn_regular='fonts/NotoSans-Regular.ttf')

# Register the Korean font
LabelBase.register(name='korean_font', fn_regular='fonts/NotoSansKR-Regular.otf')

# Register the Japnaese font
LabelBase.register(name='japanese_font', fn_regular='fonts/NotoSansJP-Regular.otf')

# Set the default font for Kivy
Config.set('kivy', 'default_font', ['default_font', 'fonts/NotoSans-Regular.ttf'])

# Load the whisper model once
model = whisper.load_model("medium")


class TranslationTextInput(TextInput):
    def __init__(self, **kwargs):
        super(TranslationTextInput, self).__init__(**kwargs)
        self.multiline = True
        self.hint_text = "Translated text will appear here"
        self.font_name = 'default_font'
        self.bind(text=self.on_text)
    
    def update_font(self, language_code):
        if language_code == 'ko':
            self.font_name = 'korean_font'
        elif language_code == 'ja':
            self.font_name = 'japanese_font'
        else:
            self.font_name = 'default_font'

    def on_text(self, instance, value):
        language_code = detect(value)
        self.update_font(language_code)



class TranscriptTextInput(TextInput):
    def __init__(self, **kwargs):
        super(TranscriptTextInput, self).__init__(**kwargs)
        self.multiline = True
        self.hint_text = "Transcribed text will appear here"
        self.font_name = 'default_font'
        self.bind(text=self.on_text)
        self.translator = Translator()
        self.stop_flag = False

    def update_font(self, language_code):
        if language_code == 'ko':
            self.font_name = 'korean_font'
        elif language_code == 'ja':
            self.font_name = 'japanese_font'
        else:
            self.font_name = 'default_font'

    def on_text(self, instance, value):
        language_code = detect(value)
        self.update_font(language_code)
    def on_touch_down(self, touch):
        if touch.button == 'right':
            self.right_click(touch)
        return super(TranscriptTextInput, self).on_touch_down(touch)

    def right_click(self, touch):
        x, y = touch.pos
        self.select_text(x, y)
        if self.selection_text:
            self.translation_text = self.translate(self.selection_text)
            app = App.get_running_app()
            app.root.translation_text.text = self.translation_text
            app.root.translation_text.update_font(detect(self.selection_text)) # Update the font for the translated text
            threading.Thread(target=self.play_text, args=(self.selection_text,)).start()

    def play_text(self, text):
        self.stop_flag = False
        lang_code = detect(text)
        self.update_font(lang_code)
        tts = gTTS(text=text, lang=lang_code, slow=False)
        tts.save("temp_speech.mp3")

        pygame.mixer.init()
        pygame.mixer.music.load("temp_speech.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            if self.stop_flag:
                pygame.mixer.music.stop()
                self.stop_flag = False
                break
            time.sleep(0.1)
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        os.remove("temp_speech.mp3")

    def stop_tts(self):
        self.stop_flag = True

    def select_text(self, x, y):
        self.cursor = self.get_cursor_from_xy(x, y)
        self.select_text(self.cursor, self.cursor)
        self.selection_to = self.cursor

    def translate(self, text):
        lang_code = detect(text)
        translated = self.translator.translate(text, dest=lang_code)
        return translated.text


class RootWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.controls_grid = ControlsGrid()
        self.add_widget(self.controls_grid)

        self.transcript_text = TranscriptTextInput()
        self.translation_text = TranslationTextInput()

        self.text_area = BoxLayout(orientation='horizontal')
        self.text_area.add_widget(self.transcript_text)
        self.text_area.add_widget(self.translation_text)

        self.add_widget(self.text_area)


class ControlsGrid(GridLayout):
    def __init__(self, **kwargs):
        super(ControlsGrid, self).__init__(**kwargs)
        self.cols = 2
        self.spacing = 10
        self.padding = 10

        select_file_button = Button(text='Select MP3 file')
        select_file_button.bind(on_release=self.select_file)
        self.add_widget(select_file_button)

        youtube_url_label = Label(text='Enter YouTube video URL')
        self.add_widget(youtube_url_label)

        self.youtube_url_entry = TextInput(hint_text='Enter YouTube URL here')
        self.add_widget(self.youtube_url_entry)

        youtube_button = Button(text='Transcribe YouTube Audio')
        youtube_button.bind(on_release=self.process_youtube_link)
        self.add_widget(youtube_button)

        self.stop_tts_button = Button(text="Stop TTS", on_press=self.stop_tts)
        self.add_widget(self.stop_tts_button)

    def stop_tts(self, instance):
        app = App.get_running_app()
        app.root.transcript_text.stop_tts()

    def select_file(self, instance):
        file_popup = Popup(title='Select an MP3 file', size_hint=(0.9, 0.9))
        file_chooser = FileChooserListView(path='/', filters=['*.mp3'])
        file_popup.add_widget(file_chooser)

        def select(instance):
            if file_chooser.selection:
                file_path = file_chooser.selection[0]
                file_popup.dismiss()
                result = model.transcribe(file_path)  # Reuse the loaded model
                text = result["text"]
                app = App.get_running_app()
                app.root.transcript_text.text = text
                app.root.transcript_text.update_font(detect(text)) # Update the font for the transcribed text
        file_chooser.bind(on_submit=select)
        file_popup.open()

    def process_youtube_link(self, instance):
        url = self.youtube_url_entry.text
        if url:
            file_path = download_audio_from_youtube(url)
            result = model.transcribe(file_path)  # Reuse the loaded model
            text = result["text"]
            app = App.get_running_app()
            app.root.transcript_text.text = text



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


class WhisperSandboxApp(App):
    def build(self):
        root_widget = RootWidget()
        return root_widget


if __name__ == '__main__':
    Window.clearcolor = (1, 1, 1, 1)
    WhisperSandboxApp().run()
