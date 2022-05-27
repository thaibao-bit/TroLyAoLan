
from selenium import webdriver
from speechtotext import SpeechToText


class App():
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path="./chromedriver")
        self.stt = SpeechToText()
    def get_youtube(self, query):
        sound = "Đang mở {} trên youtube".format(query)
        self.stt.save_and_play_sound(sound)
        self.query = query
        self.driver.get(url="https://www.youtube.com/results?search_query=" + query)
        video = self.driver.find_element_by_xpath('//*[@id="video-title"]')
        video.click()

    def get_google(self, query):
        sound = "Đang tìm {} ở google".format(query)
        self.stt.save_and_play_sound(sound)
        self.query = query
        self.driver.get(url="https://www.google.com/search?q=" + query)


        
    