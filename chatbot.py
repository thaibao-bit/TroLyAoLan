from email import message
import random
import json
import pickle
from unittest import result
import numpy as np
import YT_auto
import VApp_auto
from speechtotext import SpeechToText

import underthesea
from tensorflow.keras.models import load_model



class Bot:
    def __init__(self):    
        
        self.intents = json.load(open('intents.json'))
        self.words = pickle.load(open('words.pkl', 'rb'))
        self.labels = pickle.load(open('labels.pkl', 'rb'))
        self.model = load_model('chatbot.h5')
        
    def clean_up_sentence(self,sentence):
        sentence_words = underthesea.word_tokenize(sentence)
        sentence_words = [word.lower() for word in sentence_words]

        return sentence_words

    def bag_of_words(self,sentence):
        sentence_words = self.clean_up_sentence(sentence)
        bag = [0]* len(self.words)

        for w in sentence_words:
            for i, word in enumerate(self.words):
                if word == w:
                    bag[i] = 1
        return np.array(bag)

    def predict_label(self,sentence, *context):
        bow = self.bag_of_words(sentence)
        res = self.model.predict(np.array([bow]))[0]
        ERROR_THRESHOLD = 0.1
        result = [[i,r] for i,r in enumerate(res) if r> ERROR_THRESHOLD]

        result.sort(key=lambda x:x[1], reverse = True)
        return_list = []

        for r in result:
            return_list.append({'intent': self.labels[r[0]], 'probability': str(r[1])})
        print(" it is at ", return_list[0]['intent'], " but it should be ", context)
        return return_list

    def get_response(self,intents_list, intents_json, *context):
        tag = intents_list[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if i["tags"] == tag:
                if 'context_link' in i:
                    context = i["context_link"]
                    print("context_link: ", [c for c in i['context_link']])
                result = random.choice(i['response'])
                break
        return result, context
    def process_audio(self):
        stt = SpeechToText()
        vapp = VApp_auto.VApp()
        flag = 1
        alltext = ""
        require = ""
        answer = ""
        while flag == 1:
            message = stt.get_audio()
            alltext += "\nTôi -> " + message +"\n"
            if message == "":
                continue
            ints = self.predict_label(message)
            response = self.get_response(ints, self.intents )
            res = response[0]


            stt.save_and_play_sound(text = res)
            alltext += "Lan -> " + res +"\n"

            if ints[0]["intent"] == "youtube":
                require = stt.get_audio()
                # require = input("")
                app = YT_auto.App()
                app.get_youtube(require)
            if ints[0]["intent"] == "googlesearch":
                require = stt.get_audio()
                # require = input("")
                app = YT_auto.App()
                app.get_google(require)
            if ints[0]["intent"] == "wiki":
                require = stt.get_audio()
                # require = input("")
                answer = vapp.get_wiki(require)
            if ints[0]["intent"] == "thoitiet":
                require = stt.get_audio()
                # city = input("")
                answer = vapp.get_weather(require)
            if ints[0]["intent"] == "tambiet":
                break
            if ints[0]["intent"] == "gettime":
                answer = vapp.get_time()
            if ints[0]["intent"] == "note":
                require = stt.get_audio()
                answer = vapp.note(require)
            if ints[0]["intent"] == "readnote":
                answer = vapp.get_note()
            if ints[0]["intent"] == "tomorrownote":
                require = stt.get_audio()
                answer = vapp.tomorrow_note(require)
            if ints[0]["intent"] == "readtomorrownote":
                answer = vapp.get_tomorrow_note()
            
            if require != "":
                alltext += "Tôi -> " + require +"\n"
            if answer != "":
                alltext += "Lan -> " + answer +"\n"
                stt.save_and_play_sound(answer)
            # elif ints[0]["intent"] == "wiki":
            #     stt.save_and_play_sound(stt.wiki())
            flag = 0
        return alltext

if __name__ == "__main__":
    print("Bot is running")
    bot = Bot()
    bot.process_audio()