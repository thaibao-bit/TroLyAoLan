from gtts import gTTS
import os
from playsound import playsound
from io import BytesIO


# mp3_fp = BytesIO()

# tts = gTTS("Bánh mì sài gòn", tld="com.vn", lang="vi")

# tts.save("a2")
# playsound("a2")

# class TextToSpeech:
#     def __init__(self):
#         self.file = "a2"

# def convert(self, text):
tts = gTTS("text", tld="com.vn", lang="vi")

tts.save("a2")
playsound("a2")


# if __name__ == "__main":

#     # mtts = TextToSpeech()
#     convert("Bánh mì sài gòn")
# mp3_fp = BytesIO()
# tts = gTTS('hello', lang='en')
# tts.write_to_fp(mp3_fp)