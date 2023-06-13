import requests
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import random
import pyjokes
import os
import pyautogui

import sys
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from rain import Ui_Dialog

engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice','voice[0].id')


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()

    def run(self):
        self.TaskExecution()    

    def get_audio(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('listening..')
            r.pause_threshold=1
            r.adjust_for_ambient_noise(source,duration=1)
            audio = r.listen(source)

        try:
            print("wait for few moments.. ")
            text = r.recognize_google(audio,language='en-in')
            print(f'you just said:{text}\n')
        
        except Exception as e:
                print(e)
                speak('please tell the command again')
                text='none'

        return text
    def get_weather(self):
        api_key = '2c6b9a3ab808aed89b4b80801ffdf013'
        base_url = 'http://api.openweathermap.org/data/2.5/weather'
        city_name = self.get_audio()  # Replace with the desired city name
        
        # Send a GET request to the API
        response = requests.get(f'{base_url}?q={city_name}&appid={api_key}')
        
        # Parse the JSON response
        data = response.json()
        
        if data['cod'] == '404':
            return 'City not found'
        else:
            weather_desc = data['weather'][0]['description']
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            
            result = f"The weather in {city_name} is {weather_desc}. Temperature: {temperature} K. Humidity: {humidity}%. Wind Speed: {wind_speed} m/s."
            return result


    def wakeword(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('Rain is sleeping..')
            r.pause_threshold=1
            r.adjust_for_ambient_noise(source,duration=1)
            audio = r.listen(source)

        try:
            text = r.recognize_google(audio,language='en-in')
            print(f'wake word dected:{text}\n')
        
        except Exception as e:
                text='none'

        return text
    
    def wish(self):
        hour =int (datetime.datetime.now().hour)
        if hour >=0 and hour<12:
          print("Good morning")
          speak ("Good morning ")
        elif hour>=12 and hour<17:
          print("Good Afternoon") 
          speak("Good Afternoon")
        elif hour >=17 and hour<21:
          print("Good Evening")
          speak("Good Evening")
        else:
          print("Good Night ")
          speak("Good Night")


    def TaskExecution(self):
        while True:
            self.text= self.wakeword().lower()
            if "rain" in self.text or "rain wake up" in self.text or "wake up rain" in self.text:
                self.wish()
                speak('hello iam your rain what can i do for you')
                while True:
                        
                        self.text=self.get_audio().lower()
                        if 'play' in self.text:
                            song = self.text.replace('play', '')
                            speak('playing ' + song)
                            pywhatkit.playonyt(song)
                        elif 'skip' in self.text:
                            pyautogui.moveTo(1131,706)
                            pyautogui.leftClick()
                        elif 'pause the video' in self.text:
                            speak('pausing..')
                            pyautogui.press('space')
                        elif 'stop the video' in self.text:
                            speak('stop playing')
                            pyautogui.hotkey('ctrl','w')
                        elif 'open chrome' in self.text or 'google' in self.text:
                            speak('opening chrome')
                            os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
                        elif 'search' in self.text: 
                            query=self.get_audio()
                            pyautogui.write(query)
                            pyautogui.press('enter')           
                        elif 'exit chrome' in self.text or 'close chrome' in self.text :
                            pyautogui.hotkey('ctrl','w')
                            speak('closing google chrome')
                            break   
                        elif 'time' in self.text:
                            time = datetime.datetime.now().strftime('%I:%M %p')
                            speak('Current time is ' + time)
                        elif 'weather' in self.text:
                            speak('Please wait, getting weather information...')
                            speak('city name')
                            weather_info = self.get_weather()
                            speak(weather_info)
                            print(weather_info) 
                        elif 'hello' in self.text or 'hi' in self.text:
                            speak('hello how can i help you')
                        elif 'name' in self.text or 'call you' in self.text:
                            speak('you can call me rain')
                        elif 'how are you' in self.text:
                            speak('I am fine. You are very kind to ask')
                            speak("How are you")
                        elif 'fine' in self.text or "good" in self.text:
                            speak("It's good to know that your fine")
                        elif 'joke' in self.text:
                            speak(pyjokes.get_joke())
                        elif 'thank you' in self.text:
                            speak('you are welcome')
                        elif 'minimize' in self.text or 'minimise' in self.text:
                            pyautogui.hotkey('win','down','down')
                        elif 'close the window' in self.text:     
                            pyautogui.hotkey('ctrl','w')
                        elif 'maximize' in self.text:
                            pyautogui.hotkey('win','up','up')
                        elif 'open notepad' in self.text:
                            speak('opening notepad')
                            os.startfile('C:\\Windows\\System32\\notepad.exe')  
                            while True:
                                nquery=self.get_audio().lower()
                                if 'paste' in nquery:
                                    pyautogui.hotkey('ctrl','v')
                                elif 'save this file' in nquery:
                                    pyautogui.hotkey('ctrl','s')
                                    speak('Please specify a name for this file')
                                    nsquery=self.get_audio()
                                    pyautogui.write(nsquery)
                                    pyautogui.press('enter')
                                elif 'type' in nquery:
                                    speak('what should i write..')
                                    while True:
                                        wn=self.get_audio()
                                        if wn=='exit typing':
                                            speak('exiting')
                                            break
                                        else:
                                            pyautogui.write(wn) 
                                elif 'close notepad' in nquery:
                                    speak('closing notepad')
                                    pyautogui.hotkey('ctrl','w')

                        elif 'who i am' in self.text:
                            speak('If you talk then definetly your human.')
                        
                        elif 'story' in self.text:
                            when = ['A few years ago', 'Yesterday', 'Last night', 'A long time ago','On 20th Jan']
                            who = ['namjoon', 'Jin', 'Yoongi', 'Jhope', 'Jimin', 'Taehyung', 'Jungkook']
                            residence = ['Korea','India', 'Germany', 'Japan', 'England']
                            went = ['cinema', 'university','seminar', 'school', 'laundry']
                            happened = ['made a lot of friends','Eats a burger', 'found a secret key', 'solved a mistery', 'wrote a book']
                            speak(random.choice(when) + ', ' + random.choice(who) + ' who lived in ' + random.choice(residence) + ', went to the ' + random.choice(went) + ' and ' + random.choice(happened))
                        elif 'stop ' in self.text:
                            speak('thanks for giving me your time')
                            exit()
                        elif 'exit program' in self.text or  'stop' in self.text or 'sleep' in self.text:
                            speak('i am leaving')
                            quit()
startExecution = MainThread()
startExecution.start()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.startbut.clicked.connect(self.startTask)
        self.ui.stopbut.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QtGui.QMovie("C:\\Users\\niran\\Desktop\\rainva\\Year after year (1).gif")
        self.ui.rainm.setMovie(self.ui.movie)
        self.ui.movie.start()

        self.ui.movie = QtGui.QMovie("C:\\Users\\niran\\Desktop\\rainva\\Animated Gif.gif")
        self.ui.start.setMovie(self.ui.movie)
        self.ui.movie.start()
        
        self.ui.movie = QtGui.QMovie("C:\\Users\\niran\\Desktop\\rainva\\Angry Cloud.gif")
        self.ui.stop.setMovie(self.ui.movie)
        self.ui.movie.start()

app = QApplication(sys.argv)
rainn = Main()
rainn.show()
exit(app.exec_())