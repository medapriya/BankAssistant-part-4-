import text2speech
import speech_recognition as sr


def listen():
    r = sr.Recognizer()

    while True:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print('listening')
            while True:
                try:
                    audio = r.listen(source)
                    break
                except sr.WaitTimeoutError:
                    text2speech.speak('I am unable to hear you. Could you repeat')

            print('reading')

        try:
            text = r.recognize_google(audio)
            break
        except sr.RequestError:
            print('check your internet connection')
        except sr.UnknownValueError:
            print('Could you please speak it clearly')

    return text
