from unicodedata import name
import wikipedia
import requests
from speechtotext import SpeechToText
import unidecode
import re
import datetime 
from chatbot import *




class VApp:
    def __init__(self):
        self.stt = SpeechToText()
    def get_wiki(self, query):
        try:
            info = wikipedia.summary(query, sentences= 2)
            sound = "Bạn đợi tôi tìm hiểu về {} một lát".format(query)
            self.stt.save_and_play_sound(sound)
        except:
            return "Chủ đề bạn đưa ra chưa rõ ràng hoặc không tồn tại, bạn có cần giúp gì nữa không?"
        return info

    def remove_accent( self,text):
        return unidecode.unidecode(text)
    
    def get_time(self):
        date, time = str(datetime.datetime.now()).split()
        year = date[0:4]
        month = date[5:7]
        day = date[8:10]

        hour = time[0:2]
        minute = time[3:5]
        
        print(year, sep= "\n")
        print(time, sep= "\n")
        return "Bây giờ là {hour} giờ {minute} phút ngày {day} tháng {month} năm {year}".format(hour = hour, minute=minute, day=day, month=month,year=year) 
        # return "ok"
    
    def note(self,text):
        date, time  = str(datetime.datetime.now()).split()
        
        file_name = str(date).replace(":", "-") + "-note.txt"
        with open(file_name, "a") as f:
            f.write(text+"\n")
        return "Đã ghi {} vào danh sách của ngày hôm nay".format(text)

    def tomorrow_note(self,text):
        date, time  = str(datetime.datetime.now()+datetime.timedelta(days=1)).split()
        
        year = date[0:4]
        month = date[5:7]
        day = date[8:10]

        file_name = str(date).replace(":", "-") + "-note.txt"
        with open(file_name, "a") as f:
            f.write(text+"\n")
        return "Đã ghi {text} vào danh sách của ngày mai, ngày {day} tháng {month} năm {year}".format(text=text, day=day, month=month,year=year)

    def get_note(self):
        date, time  = str(datetime.datetime.now()).split()
        lines = []
        file_name = str(date).replace(":", "-") + "-note.txt"
        with open(file_name) as f:
            lines = f.readlines()

        count = 0
        note = ""
        for line in lines:
            count += 1
            note = note + f'ghi chú thứ {count}: {line}'
        return note

    def get_tomorrow_note(self):
        date, time  = str(datetime.datetime.now()+datetime.timedelta(days=1)).split()
        year = date[0:4]
        month = date[5:7]
        day = date[8:10]
        lines = []
        file_name = str(date).replace(":", "-") + "-note.txt"
        with open(file_name) as f:
            lines = f.readlines()

        count = 0
        note = "ngày {day} tháng {month} năm {year}".format(day=day, month=month,year=year)
        for line in lines:
            count += 1
            note = note + f'ghi chú thứ {count}: {line}'
        return note
    
    def get_weather(self, city):
        self.city = self.remove_accent(city)
        self.city = re.sub(" ","",self.city) 
        self.city = self.city.lower()
        self.apikey = "Dang ky tai khoan openweather va them apikey vao day"
        url = 'http://api.openweathermap.org/data/2.5/weather?q={city},&units=imperial&appid={apikey}'.format(city=self.city, apikey = self.apikey)
        try:
            r = requests.request("GET",url).json()
            temp = int((r['main']['temp'] - 32)* 5/9)
            max_temp = int((r['main']['temp_max'] - 32)* 5/9)
            humidity = r['main']['humidity']
            description,advice = self.convert_weather_id(int(r['weather'][0]['id']))
        except:
            return "Có một chút lỗi xảy ra hoặc địa điểm không tồn tại trong dữ liệu của tôi, bạn có cần giúp gì khác không?"
        print(r)

        
        weather = "Thời tiết ở {city} có nhiệt độ là {temp} độ c, độ ẩm là {humidity} phần trăm, trời {description}, {advice}".format(city=city,humidity = humidity ,temp = temp, description=description, advice=advice)
        return weather


    def convert_weather_id(self, id):
        description = ""
        advice = ""
        if id == 200:
            description = "giông, bão có mưa nhỏ"
            advice = "Bạn nên chú ý mang ô khi ra ngoài"
        if id == 201:
            description = "giông bão có mưa"
            advice = "Bạn nên chú ý mang ô khi ra ngoài"
        if id == 202:
            description = "giông bão với mưa lớn"
            advice = "Bạn nên chú ý mang ô khi ra ngoài"
        if id == 210:
            description = "giông bão nhẹ"
            advice = "Bạn nên chú ý khi ra ngoài"
        if id == 211:
            description = "giông bão"
            advice = "Bạn nên chú ý khi ra ngoài"
        if id == 212:
            description = "giông bão lớn"
            advice = "Bạn nên chú ý khi ra ngoài"
        if id == 221:
            description = "giông bão rải rác"
            advice = "Bạn nên chú ý khi ra ngoài"
        if id == 230:
            description = "giông bão với mưa phùn nhẹ"
            advice = "Bạn nên chú ý mang ô khi ra ngoài"
        if id == 231:
            description = "giông bão có mưa phùn"
            advice = "Bạn nên chú ý khi ra ngoài"
        if id == 232:
            description = "giông bão với mưa phùn lớn"
            advice = "Bạn nên chú ý mang ô khi ra ngoài"
        
        if id == 300:
            description = "Mưa phùn nhỏ"
            advice = "Bạn nên chú ý mang ô khi ra ngoài"
        if id == 301:
            description = "mưa phùn"
            advice = "Bạn nên chú ý mang ô khi ra ngoài"
        if id == 302:
            description = "mưa phùn dày đặc"
            advice = "Bạn nên chú ý mang ô khi ra ngoài"
        if id == 310:
            description = "mưa phùn và mưa rải rác"
            advice = "Bạn nên chú ý mang ô khi ra ngoài"
        if id == 311:
            description = "mưa phùn"
            advice = "Bạn nên chú ý mang ô khi ra ngoài"
        if id == 312:
            description = "mưa phùn và mưa nặng hạt"
            advice = "Bạn nên chú ý mang ô khi ra ngoài"
        if id == 313:
            description = "mưa rào và mưa phùn"
            advice = "Bạn nên chú ý mang ô khi ra ngoài"
        if id == 314:
            description = "mưa lớn và mưa phùn"
            advice = "Bạn nên chú ý mang ô khi ra ngoài"
        if id == 321:
            description = "mưa rào"
            advice = "Bạn nên chú ý mang ô khi ra ngoài"

        if id == 500:
            description = "mưa nhỏ"
            advice = "Bạn nên chú ý mang ô khi ra ngoài"
        if id == 501:
            description = "mưa vừa"
            advice = "Bạn nên chú ý mang ô khi ra ngoài"
        if id == 502:
            advice = "Bạn nên chú ý mang ô khi ra ngoài"
            description = "mưa lớn"
        if id == 503:
            description = "very heavy rain"
            advice = "Bạn nên chú ý mang ô khi ra ngoài"
        if id == 504:
            description = "mưa cực lớn"
            advice = "Bạn nên chú ý mang ô khi ra ngoài"
        if id == 511:
            description = "mưa đá"
            advice = "Bạn nên chú ý nguy hiểm khi ra ngoài"
        if id == 520:
            description = "mưa rào nhỏ, vừa"
            advice = "Bạn nên chú ý mang ô khi ra ngoài"
        if id == 521:
            description = "mưa rào"
            advice = "Bạn nên chú ý mang ô khi ra ngoài"
        if id == 522:
            description = "mưa rào nặng hạt"
            advice = "Bạn nên chú ý mang ô khi ra ngoài"
        if id == 531:
            description = "mưa rào rải rác"
            advice = "Bạn nên chú ý mang ô khi ra ngoài"
        if id == 600:
            description = "tuyết nhẹ"
            advice = "Bạn nên giữ ấm khi ra ngoài"
        if id == 601:
            description = "Tuyết"
            advice = "Bạn nên giữ ấm khi ra ngoài"
        if id == 602:
            description = "tuyết nhiều"
            advice = "Bạn nên giữ ấm khi ra ngoài"
        if id == 611:
            description = "mưa tuyết"
            advice = "Bạn nên giữ ấm khi ra ngoài"
        if id == 612:
            description = "mưa tuyết nhỏ"
            advice = "Bạn nên giữ ấm khi ra ngoài"
        if id == 613:
            description = "tuyết tan"
            advice = "Bạn nên giữ ấm khi ra ngoài"
        if id == 615:
            description = "Mưa nhẹ và tuyết"
            advice = "Bạn nên giữ ấm khi ra ngoài"
        if id == 616:
            description = "mưa và tuyết"
            advice = "Bạn nên giữ ấm khi ra ngoài"
        if id == 620:
            description = "Mưa tuyết nhẹ"
            advice = "Bạn nên giữ ấm khi ra ngoài"
        if id == 621:
            description = "mưa tuyết"
            advice = "Bạn nên giữ ấm khi ra ngoài"
        if id == 622:
            description = "Mưa tuyết lớn"
            advice = "Bạn nên giữ ấm khi ra ngoài"
        if id == 701:
            description = "sương mù"
            advice = "Bạn nên cẩn thận tầm nhìn khi lái xe"
        if id == 711:
            description = "nhiều sương"
            advice = "Bạn nên cẩn thận tầm nhìn khi lái xe"
        if id == 721:
            description = "sương mù dày đặc"
            advice = "Bạn nên cẩn thận tầm nhìn khi lái xe"
        if id == 731:
            description = "cát / bụi xoáy"
            advice = "Bạn không nên ra ngoài vào thời gian này"
        if id == 741:
            description = "sương ẩm"
            advice = "Bạn nên cẩn thận tầm nhìn khi lái xe"
        if id == 751:
            description = "có cát"
            advice = "Bạn nên cẩn thận tầm nhìn khi lái xe"
        if id == 761:
            description = "bụi mù"
            advice = "Bạn nên cẩn thận tầm nhìn khi lái xe"
        if id == 762:
            description = "có tro núi lửa"
            advice = "Bạn không nên ra ngoài vào thời gian này"
        if id == 771:
            description = "mưa đá"
            advice = "Bạn nên cẩn thận khi ra ngoài"
        if id == 781:
            description = "có lốc xoáy"
            advice = "Bạn không nên ra ngoài vào thời gian này"
        if id == 800:
            description = "quang đãng"
            advice = "Thời tiết này rất phù hợp để đi chơi một ngày nhỉ"
        if id == 801:
            description = "ít mây"
            advice = "Thời tiết này rất phù hợp để đi chơi một ngày nhỉ"
        if id == 802:
            description = "mây rải rác"
            advice = "Chúc bạn một ngày tốt lành"
        if id == 803:
            description = "nhiều mây"
            advice = "Chúc bạn một ngày tốt lành"
        if id == 804:
            description = "mây u ám"
            advice = "Bạn nên chú ý mang ô phòng trường hợp có mưa "
        return description,advice

# if __name__ == "__main__":
#     vapp = VApp()
#     vapp.get_time()
