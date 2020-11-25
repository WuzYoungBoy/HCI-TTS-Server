from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/text-to-speech')
def text_to_speech():
    return 'text-to-speech'


@app.route('/audio-to-text')
def audio_to_text():
    return 'audio-to-text'

if __name__=="__main__":
    app.run(debug = True)