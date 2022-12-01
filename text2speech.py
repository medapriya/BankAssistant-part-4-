import os
from gtts import gTTS

from playsound import playsound


# playsound == 1.2.2
def speak(mytext):
    print(mytext)
    language = 'en'
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("temp.mp3")
    playsound("temp.mp3")
    os.system("del temp.mp3")
