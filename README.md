# whisper-sandbox

This is just a sandbox for me to try out Whisper (https://openai.com/research/whisper).

```python
import whisper

model = whisper.load_model("tiny")
result = model.transcribe("audio/The Truth About Learning a Language (That Many Don’t Want to Hear).mp3")
print(result["text"])
```

~Adam Martinez
March 18, 2023