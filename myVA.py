from curses import window
from tkinter import *
from speechtotext import *
from chatbot import *
import YT_auto
import VApp_auto
from PIL import ImageTk, Image 


class VirtualAssistant:
  def __init__(self):
      self.bot = Bot()
      self.stt = SpeechToText()

  
  def wikipedia_screen(self,text):


    wikipedia_screen = Toplevel(screen)
    wikipedia_screen.title(text)
    wikipedia_screen.iconbitmap('app_icon.ico')

    message = Message(wikipedia_screen, text= text)
    message.pack()

  def update_txt(self):
    txt.insert(END,self.bot.process_audio())

  def main_screen(self):

    global screen
    screen = Tk()
    screen.title("Trợ lý ảo Lan")
    screen.geometry("700x400")

    bg = PhotoImage(file = "bg.png")

    canvas1 = Canvas( screen, width = 700,
                    height = 400)
      
    canvas1.place(x=0,y=0)
    global txt
    txt = Text(screen, bg="#17202A", fg="#EAECEE", font= "Helvetica 14", width=45)
    txt.insert(END,"Xin chào, tôi là Lan, trợ lý ảo của bạn.")
    txt.place(x=10,y=10)
    scrollbar = Scrollbar(txt)
    scrollbar.place(relheight=1, relx=0.974)

    va = PhotoImage(file="VietnameseVA.png")
    
    microphone_photo = PhotoImage(file = "logo.png")
    microphone_button = Button(screen, image=microphone_photo, command = self.update_txt)

    settings_photo = PhotoImage(file = "settings.png")
    settings_button = Button(screen,image=settings_photo, command = self.update_txt)
    
    info_button = Button(screen,text ="Info", command = self.bot.process_audio)


    # Display 
    canvas1.create_image( 0, 0, image = bg, 
                        anchor = "nw")
    canvas1.create_image( 445, 145, 
                                    anchor = "nw",
                                    image = va)
    canvas1.create_window( 500, 0, 
                                    anchor = "nw",
                                    window = microphone_button)
    canvas1.create_window( 640, 0, 
                                    anchor = "nw",
                                    window = settings_button)
    canvas1.create_window( 650, 65, 
                                    anchor = "nw",
                                    window = info_button) 
                                  
    # info_button.pack(pady=10,side=BOTTOM)
    # self.stt.save_and_play_sound("Xin chào, tôi là Lan, trợ lý ảo của bạn.")
    screen.mainloop()

if __name__ == "__main__":
  va = VirtualAssistant()
  va.main_screen()
