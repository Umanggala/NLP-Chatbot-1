from gtts import *
import os
import get_response

tts = gTTS(text="Hello World",lang='en')
tts.save('response.mp3')
os.system("mpg321 hello.mp3")
