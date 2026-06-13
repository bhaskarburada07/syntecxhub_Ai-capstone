# requirements.txt
"""
opencv-python==4.8.1.78
face-recognition==1.3.0
numpy==1.24.3
SpeechRecognition==3.10.0
pyttsx3==2.90
pyaudio==0.2.11
Pillow==10.0.0
"""

# face_auth/__init__.py
from .register import FaceRegister
from .authenticate import FaceAuthenticator
__all__ = ['FaceRegister', 'FaceAuthenticator']

# face_auth/register.py
import cv2,os,numpy as np
from face_recognition import face_encodings
class FaceRegister:
    def __init__(self,db="database/users"):self.db=db;self.face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml');os.makedirs(db,exist_ok=True)
    def register_user(self,name):
        print(f"\n[REGISTER] {name}\nPress SPACE to capture (20 needed), Q to quit")
        cap=cv2.VideoCapture(0);count=0
        while True:
            ret,frame=cap.read()
            if not ret:break
            gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            faces=self.face_cascade.detectMultiScale(gray,1.3,5)
            for(x,y,w,h)in faces:cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(frame,f"{count}/20",(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)
            cv2.imshow('Register',frame)
            key=cv2.waitKey(1)&0xFF
            if key==ord(' ')and len(faces)>0:
                x,y,w,h=faces[0];face=frame[y:y+h,x:x+w]
                if face.size>0:
                    face=cv2.resize(face,(150,150));count+=1
                    os.makedirs(f"{self.db}/{name}",exist_ok=True)
                    cv2.imwrite(f"{self.db}/{name}/face_{count}.jpg",face)
                    print(f"Captured {count}/20")
                    if count>=20:break
            elif key==ord('q'):break
        cap.release();cv2.destroyAllWindows()
        return count>=20
    def get_registered_users(self):
        if not os.path.exists(self.db):return[]
        return[d for d in os.listdir(self.db)if os.path.isdir(os.path.join(self.db,d))]

# face_auth/authenticate.py
import cv2,os,numpy as np,face_recognition
class FaceAuthenticator:
    def __init__(self,db="database/users"):
        self.db=db;self.known_encodings=[];self.known_names=[]
        self.load_faces()
    def load_faces(self):
        if not os.path.exists(self.db):return
        for name in os.listdir(self.db):
            encodings=[]
            for img in os.listdir(f"{self.db}/{name}"):
                if img.endswith(('.jpg','.png')):
                    img_path=f"{self.db}/{name}/{img}"
                    image=face_recognition.load_image_file(img_path)
                    if enc:=face_recognition.face_encodings(image):
                        encodings.append(enc[0])
            if encodings:
                self.known_encodings.append(np.mean(encodings,axis=0))
                self.known_names.append(name)
                print(f"Loaded {len(encodings)} images for {name}")
    def authenticate(self):
        print("\n[AUTH] Look at camera (Q to quit)")
        cap=cv2.VideoCapture(0);attempts=0
        while attempts<30:
            ret,frame=cap.read()
            if not ret:break
            small=cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
            rgb=cv2.cvtColor(small,cv2.COLOR_BGR2RGB)
            locations=face_recognition.face_locations(rgb)
            encodings=face_recognition.face_encodings(rgb,locations)
            for enc in encodings:
                matches=face_recognition.compare_faces(self.known_encodings,enc,0.6)
                if True in matches:
                    name=self.known_names[matches.index(True)]
                    print(f"\n✅ Authenticated: {name}")
                    cap.release();cv2.destroyAllWindows()
                    return name
            cv2.imshow('Auth',frame)
            if cv2.waitKey(1)&0xFF==ord('q'):break
            attempts+=1
        cap.release();cv2.destroyAllWindows()
        print("\n❌ Authentication failed")
        return None

# chatbot/intents.py
import random
INTENTS={
    "greeting":{"patterns":["hello","hi","hey"],"responses":["Hello! How can I help?","Hi there!"]},
    "who_are_you":{"patterns":["who are you","your name"],"responses":["I'm your AI Assistant"]},
    "open_calculator":{"patterns":["open calculator","calc"],"responses":["Opening Calculator..."]},
    "open_notepad":{"patterns":["open notepad","notepad"],"responses":["Opening Notepad..."]},
    "open_chrome":{"patterns":["open chrome","chrome"],"responses":["Opening Chrome..."]},
    "open_youtube":{"patterns":["open youtube","youtube"],"responses":["Opening YouTube..."]},
    "open_google":{"patterns":["open google","google"],"responses":["Opening Google..."]},
    "current_time":{"patterns":["current time","what time is it","time now"],"responses":["Current time:"]},
    "current_date":{"patterns":["current date","today's date"],"responses":["Today's date:"]},
    "exit":{"patterns":["exit","quit","goodbye"],"responses":["Goodbye!"]},
    "help":{"patterns":["help","commands"],"responses":["Commands: calculator, notepad, chrome, youtube, google, time, date, exit"]}
}
def get_intent(cmd):
    cmd=cmd.lower()
    for intent,data in INTENTS.items():
        for pattern in data["patterns"]:
            if pattern in cmd:return intent
    return "unknown"
def get_response(intent):
    if intent in INTENTS:return random.choice(INTENTS[intent]["responses"])
    return "Unknown command. Type 'help'"

# chatbot/chatbot.py
from .intents import get_intent,get_response
class RuleBasedChatbot:
    def process_command(self,cmd):
        intent=get_intent(cmd)
        return{"intent":intent,"response":get_response(intent),"command":cmd}
    def should_execute(self,intent):
        return intent in["open_calculator","open_notepad","open_chrome","open_youtube","open_google","current_time","current_date","exit"]

# commands/executor.py
import subprocess,os,webbrowser
from datetime import datetime
import pyttsx3
class CommandExecutor:
    def __init__(self):
        self.engine=pyttsx3.init();self.engine.setProperty('rate',150)
    def speak(self,text):print(f"Assistant: {text}");self.engine.say(text);self.engine.runAndWait()
    def execute(self,intent):
        try:
            if intent=="open_calculator":subprocess.Popen("calc.exe");return"Calculator opened"
            if intent=="open_notepad":subprocess.Popen("notepad.exe");return"Notepad opened"
            if intent=="open_chrome":
                for path in["C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe","C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"]:
                    if os.path.exists(path):subprocess.Popen([path]);return"Chrome opened"
                webbrowser.open("https://www.google.com");return"Chrome opened"
            if intent=="open_youtube":webbrowser.open("https://www.youtube.com");return"YouTube opened"
            if intent=="open_google":webbrowser.open("https://www.google.com");return"Google opened"
            if intent=="current_time":return f"The time is {datetime.now().strftime('%I:%M %p')}"
            if intent=="current_date":return f"Today is {datetime.now().strftime('%B %d, %Y')}"
            if intent=="exit":return"Exiting..."
            return"Unknown command"
        except Exception as e:return f"Error: {e}"

# voice/speech_input.py
import speech_recognition as sr
class SpeechInput:
    def __init__(self):
        self.r=sr.Recognizer()
        with sr.Microphone() as source:self.r.adjust_for_ambient_noise(source,duration=1)
        print("🎤 Microphone ready")
    def listen(self,timeout=5):
        print("\n[VOICE] Listening... (say 'cancel' to stop)")
        try:
            with sr.Microphone() as source:audio=self.r.listen(source,timeout=timeout,phrase_time_limit=5)
            text=self.r.recognize_google(audio);print(f"You said: {text}")
            return None if text.lower()=="cancel" else text.lower()
        except:return None

# main.py
import sys,os
from face_auth import FaceRegister,FaceAuthenticator
from chatbot import RuleBasedChatbot
from commands import CommandExecutor
from voice import SpeechInput

class AISmartAssistant:
    def __init__(self):
        self.register=FaceRegister()
        self.auth=FaceAuthenticator()
        self.chatbot=RuleBasedChatbot()
        self.executor=CommandExecutor()
        self.voice=SpeechInput()
        self.user=None
    def clear(self):os.system('cls' if os.name=='nt' else 'clear')
    def menu(self):
        print("\n"+"="*50);print("🤖 AI SMART ASSISTANT");print("="*50)
        print("1. 📝 Register Face\n2. 🔐 Authenticate\n3. 🎤 Voice Mode\n4. ⌨️ Text Mode\n5. 🚪 Exit")
        print("="*50);print(f"✅ User: {self.user or 'Not authenticated'}")
    def process(self,cmd,voice=False):
        if not cmd:return True
        res=self.chatbot.process_command(cmd)
        if voice:self.executor.speak(res["response"])
        else:print(f"\nAssistant: {res['response']}")
        if self.chatbot.should_execute(res["intent"]):
            result=self.executor.execute(res["intent"])
            if voice:self.executor.speak(result)
            else:print(f"System: {result}")
            return False if res["intent"]=="exit" else True
        return True
    def run(self):
        while True:
            self.menu()
            choice=input("\nChoice (1-5): ").strip()
            if choice=='1':
                name=input("Enter name: ").strip()
                if self.register.register_user(name):print(f"✅ Registered {name}")
                else:print("❌ Registration failed")
                self.auth=FaceAuthenticator()
            elif choice=='2':
                self.user=self.auth.authenticate()
                if self.user:self.executor.speak(f"Welcome {self.user}")
            elif choice=='3':
                if not self.user:print("❌ Authenticate first");input();self.clear();continue
                print("\n[VOICE MODE] Say commands (or 'menu'/'exit')")
                while True:
                    cmd=self.voice.listen()
                    if not cmd:continue
                    if cmd=="menu":break
                    if cmd=="exit":sys.exit(0)
                    if not self.process(cmd,voice=True):sys.exit(0)
            elif choice=='4':
                if not self.user:print("❌ Authenticate first");input();self.clear();continue
                print("\n[TEXT MODE] Commands: hello, who are you, open calculator/notepad/chrome/youtube/google, current time/date, help, exit")
                while True:
                    cmd=input("\nYou: ").strip().lower()
                    if cmd=="menu":break
                    if cmd=="exit":self.executor.execute("exit");sys.exit(0)
                    if cmd and not self.process(cmd):sys.exit(0)
            elif choice=='5':print("Goodbye!");sys.exit(0)
            else:print("Invalid choice")
            input("\nPress Enter...");self.clear()

if __name__=="__main__":
    try:AISmartAssistant().run()
    except KeyboardInterrupt:print("\nGoodbye!")