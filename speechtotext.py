import speech_recognition as sr
from gtts import gTTS
import os
from playsound import playsound
import wikipedia


class SpeechToText:
    def __init__(self):
        self.bot = "Bot: "
        self.name = "Chồng yêu"
        self.botname = "Em"
        self.repeat = "" + self.botname +" nghe không rõ, "+ self.name +" nói lại " + self.botname +" nghe được không ?"
        wikipedia.set_lang("vi")
    def get_audio(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Tôi: ", end='')
            audio = r.listen(source, phrase_time_limit=3)
            try:
                text = r.recognize_google(audio, language="vi-VN")
                print(text)
                return text
            except:
                print("...")
                return ""

    def answer(self, text):
        print(self.bot + text)

    def save_and_play_sound(self, text):

        tts = gTTS(text, tld="com.vn", lang="vi")
        # self.answer(text)
        tts.save("a2")
        playsound("a2")

    def think(self, audio):
        if "khỏe không" in audio:
            text = "" + self.botname +" vẫn đầy pin và kết nối internet đầy đủ, " + self.botname +" có thể giúp gì không?"
        elif "ai" and "đẹp trai" and "nhất thế giới" in audio:
            text ="Đương nhiên là anh đẹp trai nhất rồi, anh Bảo ạ !"

        elif "em" and "ngủ đi" in audio:
            text = "Bai bai " + self.name +"  "

        elif "thông tin" in audio:
            
            text = self.wiki()
            if text == "" + self.botname +" không nghe thấy gì cả, " + self.name +" có cần " + self.botname +" giúp gì nưã không?":
                text = self.wiki() 
            # text += ". Đó là tất cả những gì " + self.botname +" biết, anh có cần giúp gì nữa không?"

        elif(audio == "bánh mì bơ sưã đặc ruột thơm ngon"):
            text = "đương nhiên là thằng Ái"
        
        else:
            text = self.name + " ơi! " + self.repeat
        return text
    
    def wiki(self):
        self.save_and_play_sound("" + self.name +"   cần tìm hiểu chủ đề gì nè?")
        w = sr.Recognizer()
        topic = self.get_audio()
        if topic != "":
            self.save_and_play_sound("" + self.name +" đợi " + self.botname +" tìm hiểu về " + topic +" một lát")
            info = wikipedia.summary(topic, sentences= 2)
            return info
        else :
            return "" + self.botname +" không nghe thấy gì cả, " + self.name +" có cần " + self.botname +" giúp gì nữa không?"
    def run(self):
        self.save_and_play_sound("chào " + self.name +"  ," + self.name+" có khoẻ không?")
        while(True):
            text = self.think(self.get_audio())
            
            self.save_and_play_sound(text)
            if text == "Bai bai " + self.name +"  ":
                break

        
            



if __name__ == "__main__":
    stt = SpeechToText()
    text = stt.run()
    

# r = sr.Recognizer()

# with sr.AudioFile(filename) as source:
#     # listen for the data (load audio to memory)
#     audio_data = r.record(source)
#     # recognize (convert from speech to text)
#     text = r.recognize_google(audio_data)
#     print(text)
