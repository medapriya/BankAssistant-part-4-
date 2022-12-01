import os
import time
import datetime
import threading
import dialogflow
from db_mang import get_dbdata
from face_det import Face
from speech2text import listen
from text2speech import speak
from google.api_core.exceptions import InvalidArgument

# dialogflow==0.5.1
# google-api-core==1.4.1

os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"] = r'C:\Users\RITISHREDDY\Madhu\bank_assistant\bankhelper-whlr-0bd71af685ed.json'
DIALOGFLOW_PROJECT_ID = 'bankhelper-whlr'
DIALOGFLOW_LANGUAGE_CODE = 'en'
SESSION_ID = 'me'
myFace = Face()


def chat(text_to_be_analyzed, fid, name):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)

    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise

    resp = response.query_result.fulfillment_messages

    output_text = resp[0].text.text[0]
    if output_text.__contains__('db'):
        output_text = get_dbdata(name, output_text.split('db ')[1])
        print(output_text)

    print('User :', response.query_result.query_text)
    fid.write('User :'+ response.query_result.query_text + '\n')
    print('Bot :', end='')
    speak(output_text)
    fid.write('Bot :'+ output_text + '\n')
    print('###################')
    fid.write('###################\n')

    return output_text[len(output_text) - 2: len(output_text)] == ':)'


def chat_bot():
    current_time = datetime.datetime.now()
    fid = open('log\log' + str(current_time.hour) + str(current_time.minute) + str(current_time.second) + '.txt','w+')
    print('*' * 60)
    fid.write('*' * 60 + '\n')
    speak('\t\tWelcome to Fedral Bank')
    fid.write('\t\tWelcome to Fedral Bank\n')
    print('*' * 60)
    fid.write('*' * 60 + '\n')
    
    time.sleep(4)
    if not myFace.get_name() == 'Unknown':
        speak('Hello ' + myFace.get_name())
        fid.write('Hello' + myFace.get_name() + '\n')
    else:
        speak('Hello there')
        speak('Get you face registered')
        fid.write('Hello' + '\n')
        myFace.exit_threads = False

    while True:
        if not myFace.exit_threads:
            text = listen()
            if text == 'quit':
                speak('We are happy to serve you. \nThanks for visiting. \nPlease visit again.')
                fid.write('We are happy to serve you. \nThanks for visiting. \nPlease visit again.\n')
                fid.close()
                current_time = datetime.datetime.now()
                fid = open('log\log' + str(current_time.hour) + str(current_time.minute) + str(current_time.second) + '.txt','w+')
                break
            else:
                print(text)
                if chat(text, fid, myFace.get_name()):
                    break
        else:
            speak('We are happy to serve you. \nThanks for visiting. \nPlease visit again.')
            fid.write('We are happy to serve you. \nThanks for visiting. \nPlease visit again.\n')
            fid.close()
            current_time = datetime.datetime.now()
            fid = open('log\log' + str(current_time.hour) + str(current_time.minute) + str(current_time.second) + '.txt', 'w+')
            break


t1 = threading.Thread(target=myFace.start_stream)
t2 = threading.Thread(target=myFace.face_rec)
t3 = threading.Thread(target=chat_bot)

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()

# chat_bot()
