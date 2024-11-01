from flask import Flask, render_template
import whisper
import tiktoken

app = Flask(__name__)

#load model for speech recognition and transcribing 'turbo' or 'large' (all others for whisper are english only)
model = whisper.load_model("turbo")

enc = tiktoken.get_encoding("o200k_base")
assert enc.decode(enc.encode("hello world")) == "hello world" 
# To get the tokeniser corresponding to a specific model in the OpenAI API:
enc = tiktoken.encoding_for_model("gpt-4o")

#transcribe audio file
#result = model.transcribe("files/audio.m4a")

#testing translating
result = model.transcribe("files/audio.m4a", task='translate', language='Spanish') 

print(result["text"])

# Home page
@app.route('/')
def home():
    return render_template('index.html')    

if __name__ == "__main__":
     app.run(debug=True)