from flask import Flask,request,jsonify
from gtts import gTTS
from tempfile import TemporaryFile
from pydub import AudioSegment
import urllib.request as urllib_requst
import speech_recognition as sr
import base64


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/text-to-speech', methods = ['POST', 'GET'])
def text_to_speech():

    request_json = request.get_json()

    if request_json != None:
        
        try:
            myText = request_json['text']
            language="en"
            out = gTTS(text=myText, lang=language, slow=False)
            f = TemporaryFile()
            out.write_to_fp(f)
            f.seek(0)
            audio=f.read()
            audio=base64.b64encode(audio)

            f.close()        
            # audio = 'data:audio/wab;base64,' + audio
            return jsonify({'src': audio, 'message':'TTS Success' ,'status':'successed'}),200

        except Exception as e :
            return jsonify({'src': None, 'message':'TTS Conversion Failed: ' + str(e) ,'status':'Failed'}),400  

    else:
        return jsonify({'src': None,'message':'Request JSON Not Found' , 'status':'Failed'}),400


    return 'text-to-speech'


@app.route('/speech-to-text', methods = ['POST','GET'])
def speech_to_text():

    request_json = request.get_json()
    if request_json != None:

        try:

            url = request_json['url']
            
            # header = {'User-Agent': 'Mozilla/5.0'}
            # req = urllib_requst.Request(url, headers = header)        
            # u = urllib_requst.urlopen(req)

            local_filename,headers = urllib_requst.urlretrieve(url)
            audio_type = headers['Content-Type']

            sound = AudioSegment.from_file(local_filename)
            sound.export(local_filename, format= "wav")

            r = sr.Recognizer()
            with sr.AudioFile(local_filename) as audio_file:
                audio_content = r.record(audio_file)

            text=r.recognize_google(audio_content)

            return jsonify({'text': text,'message':'STT Conversion Success', 'status':'successed'}),200

        except Exception as e :
            return jsonify({'text': None, 'message':'STT Conversion Failed: ' + str(e) ,'status':'Failed'}),400    
    else:
        return jsonify({'text': None, 'message':'Request JSON Not Found' ,'status':'Failed'}),400


# if __name__=="__main__":
#     app.run(debug=True)   

 