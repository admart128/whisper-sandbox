import whisper

model = whisper.load_model("tiny")
result = model.transcribe("audio/The Truth About Learning a Language (That Many Don’t Want to Hear).mp3")
print(result["text"])