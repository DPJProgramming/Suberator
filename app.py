#from flask import Flask, render_template
import whisper
import tiktoken
import subprocess
import pysubs2

#app = Flask(__name__)

#load model for speech recognition and transcribing 'turbo' or 'large' (all others for whisper are english only)
model = whisper.load_model("turbo")

#initialize tokeniser
enc = tiktoken.get_encoding("o200k_base")
# Test the tokeniser
#assert enc.decode(enc.encode("hello world")) == "hello world" 
# get tokeniser corresponding to a specific OpenAI API model
enc = tiktoken.encoding_for_model("gpt-4o")

#extract audio from video file
videoPath = "files/video.mp4"
audioPath = "files/audio.wav"
ffmpegExtract = ["ffmpeg", "-i", videoPath, "-q:a", "0", "-map", "a", audioPath, "-y"]
subprocess.run(ffmpegExtract, check=True)

#transcribe audio file
result = model.transcribe(audioPath)
print(result["text"])

#create subtitle file
subs = pysubs2.SSAFile()

for subLine in result["segments"]:
    #get start and end time of subtitle line
    start_time = subLine["start"]
    end_time = subLine["end"]
    text = subLine["text"]

    #format and add subtitle line to file
    line = pysubs2.SSAEvent(start=start_time, end=end_time, text=text) 
    subs.events.append(line)   
    print(f"{start_time} --> {end_time} {text}")

#save subtitle file
subs.save("files/subtitles.srt", format_='srt')

#testing translating
#resultSpanish = model.transcribe(audioPath, task='translate', language='Spanish') 
#print(resultSpanish["text"])

subtitle_file = "files/subtitles.srt"
output_video = "files/output_video.mp4"

# FFmpeg command to add subtitles
ffmpeg_command = [
    "ffmpeg",
    "-i", videoPath,  # Input video file
    "-i", subtitle_file,    # Subtitle file
    "-c:v", "libx264",       # Use libx264 codec for video encoding
    "-c:a", "copy",          # Copy the audio stream without re-encoding
    "-vf", f"subtitles={subtitle_file}",  # Apply subtitles filter to burn subtitles into video
    "-y",                    # Overwrite output file if it exists
    output_video        # Output video file
]

subprocess.run(ffmpeg_command, check=True)



# Home page
# @app.route('/')
# def home():
#     return render_template('index.html')    

# if __name__ == "__main__":
#      app.run(debug=True)