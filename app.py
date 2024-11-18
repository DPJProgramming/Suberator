from flask import Flask, render_template, request
import whisper
import tiktoken
import subprocess
import pysubs2

app = Flask(__name__)

# #testing translating
# #resultSpanish = model.transcribe(audioPath, task='translate', language='Spanish') 
# #print(resultSpanish["text"])

#Home page
@app.route('/')
def home():
    return render_template('index.html')    

@app.route('/transcribe', methods=['POST'])
def transcribe():
    print("reached transcribe")
    print()
    print()
    print()

    #save uploaded file
    file = request.files['video']
    videoPath = "files/video.mp4"
    file.save(videoPath)

    #load model for speech recognition and transcribing 'turbo' or 'large' (all others for whisper are english only)
    model = whisper.load_model("turbo")

    #initialize tokeniser
    enc = tiktoken.get_encoding("o200k_base")
    # get tokeniser corresponding to a specific OpenAI API model
    enc = tiktoken.encoding_for_model("gpt-4o")

    #extract audio from video file
    audioPath = "files/audio.wav"
    ffmpegExtract = ["ffmpeg", "-i", videoPath, "-q:a", "0", "-map", "a", audioPath, "-y"]
    subprocess.run(ffmpegExtract, check=True)

    #transcribe audio file
    result = model.transcribe(audioPath, word_timestamps=True)
    #print(result["text"])

    # create subtitle file
    return createSubs(result, videoPath)

def createSubs(result, videoPath):
    print("reached createSubs")
    print()
    print()
    print()

    #create subtitle file 
    subs = pysubs2.SSAFile()

    for subLine in result["segments"]:
        # Iterate through words in the segment (use subLine["words"])
        for word in subLine["words"]: 
            wordText = word["word"]
            wordStart = word["start"]
            wordEnd = word["end"]

        # Get start and end time of subtitle line
        start_time = subLine["start"]
        end_time = subLine["end"]
        text = subLine["text"]

        # Convert start and end time to milliseconds
        start_ms = int(start_time * 1500)
        end_ms = int(end_time * 1500)

        # Format and add subtitle line to file
        line = pysubs2.SSAEvent(start=start_ms, end=end_ms, text=text) 
        subs.events.append(line)

    #save subtitle file
    subs.save("files/subtitles.srt", format_='srt')

    #add subtitles to video
    return addSubs(videoPath)

def addSubs(videoPath):
    print("reached add subs")
    print()
    print()
    print()

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

    # Run FFmpeg command
    subprocess.run(ffmpeg_command, check=True)
    
    return "success!"
    

if __name__ == "__main__":
     app.run(debug=True)