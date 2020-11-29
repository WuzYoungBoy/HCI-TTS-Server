from flask import Flask,request,jsonify
import urllib.request as urllib_requst
import base64


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/text-to-speech')
def text_to_speech():
    request_json = request.get_json()

    if request_json != None:
    
        text = request_json['text']
        return text
    else:
        return 'None'


    return 'text-to-speech'


@app.route('/audio-to-text', methods = ['POST','GET'])
def audio_to_text():

    request_json = request.get_json()

    if request_json != None:
        
        header = {'User-Agent': 'Mozilla/5.0'}
        
        req = urllib_requst.Request(request_json['url'], headers = header)
        url = urllib_requst.urlopen(req)
        data = url.read(1024)

        content = data
        while data:
            data = url.read(1024)
            content += data

        content = base64.b64encode(content)
        return content
    else:
        return 'None'

if __name__=="__main__":
    app.run(debug = True)