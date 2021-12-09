import speech_recognition as sr
from gtts import gTTS
import playsound
import os
import time
from time import ctime
import re
import webbrowser
import smtplib
def listen():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("I am listening..")
        audio=r.listen(source,phrase_time_limit=5)
    data=""
    try:
        data=r.recognize_google(audio,language='en-US')
        print("You said:"+data)
    except sr.UnknownValueError:
        print("I cannot hear you")
    except sr.RequestError as e:
        print("Request Failed")
    return data
def respond(String):
    print(String)
    tts=gTTS(text=String,lang="en")
    tts.save("respond.mp3")
    playsound.playsound("respond.mp3")
    os.remove("respond.mp3")
def voice_assistant(data):
    if "how are you" in data:
        listening = True
        respond("I am well")
    if "time" in data:
        listening  = True
        respond(ctime())

    if "open google" in data.casefold():
        listening =True
        reg_ex = re.search('open google(.*)',data)
        url = 'https://www.google.com/'
        if reg_ex:
            sub = reg_ex.group(1)
            url = url + 'r/'
        webbrowser.open(url)
        print('Done')
        respond('Done')

    if "email" in data:
        listening = True
        respond("Whom should i send email to?")
        to = listen()
        edict = {'Sai':'saiprasaad1999@gmail.com','Naga':'nagarajan17699@gmail.com'}
        toaddr = edict[to]
        respond("What is the Subject?")
        subject = listen()
        respond("What should i tell that person")
        message = listen()
        content = 'Subject: {}\n\n{}'.format(subject,message)
        mail = smtplib.SMTP('smtp.gmail.com',587)
        mail.ehlo()
        mail.starttls()
        mail.login('saiprasaad.k@gmail.com','sairam1999')
        mail.sendmail('saiprasaad.k@gmail.com',toaddr,content)
        mail.close()
        respond('Email Sent')

    if "wiki" in data.casefold():
        listening = True
        respond("What should I search?")
        query = listen()
        response = requests.get("https://en.wikipedia.org/wiki/" +query)
        if response is not None:
            html = bs4.BeautifulSoup(response.text,'html.parser')
            paragraphs = html.select("p")
            intro = [i.text for i in paragraphs]
            halo = ''.join(intro)
        respond(halo[:200])

    if "stop" in data:
        listening = False
        print("Listening Stopped")
        respond("See you Sai")

    try:
        return listening
    except UnboundLocalError:
        print("timed out")
        
    
time.sleep(2)
respond("Hello Saiprasaad,what can I do for you?")
listening = True
while listening == True:
    data = listen()#call the listen() here
    listening = voice_assistant(data)
