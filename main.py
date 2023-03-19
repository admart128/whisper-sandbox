import whisper
import tkinter as tk
from tkinter import filedialog

window = tk.Tk()
window.title("whisper-sandbox")
window.geometry("750x750")

filename = ""

def select_file():
    file_path = filedialog.askopenfilename(
        initialdir="/", title="Select A File", filetypes=(("mp3 files", "*.mp3"),))
    model = whisper.load_model("medium")
    result = model.transcribe(file_path)
    text = result["text"]
    output_text.delete('1.0', tk.END)
    output_text.insert(tk.END, text)

button = tk.Button(window, text="Select MP3 File", command=select_file)
button.pack()

output_text = tk.Text(window, height=40, width=80)
output_text.pack()

window.mainloop()