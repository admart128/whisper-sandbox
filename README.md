# whisper-sandbox

<h1>Overview</h1>

This program is a GUI application that transcribes audio from an MP3 file or a YouTube video using the Whisper ASR model. It also provides translation functionality for the transcribed text.

<h1>Dependencies</h1>

<p>
whisper 
<p>
tkinter 
<p>
googletrans 
<p>
yt-dlp 
<p>
tempfile 
<p>
os
<p>

<h1>Functions</h1>

download_audio_from_youtube(url): Downloads audio from a YouTube video and returns the path of the downloaded file.

select_file(): Opens a file dialog to select an MP3 file, transcribes the audio, and displays the transcribed text.

process_youtube_link(): Processes the YouTube link

<h1>User Instructions</h1>

Select an mp3 file or paste a link to a YouTube video with Korean or Japanese-language audio and the program will transcribe the audio into the transcription field.

(Other languages may work, but aren't officially supported for this application.)

Highlight any text in the transcription field at it will be translated dnyamically in the translation field below.

<h1>Credit</h1>

Thank you for using this application!

Author: Adam Martinez
Date: March 18, 2023