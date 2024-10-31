from flask import Flask, render_template
import whisper
import tiktoken

#load model for speech recognition and transcribing 'turbo' or 'large' (all others for whisper are english only)
model = whisper.load_model("base")

enc = tiktoken.get_encoding("o200k_base")
assert enc.decode(enc.encode("hello world")) == "hello world" 

# To get the tokeniser corresponding to a specific model in the OpenAI API:
enc = tiktoken.encoding_for_model("gpt-4o")

result = model.transcribe("files/audio.m4a")
print(result["text"])


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Render the HTML page

if __name__ == "__main__":
     app.run(debug=True)