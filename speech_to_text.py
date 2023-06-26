import speech_recognition as sr
import requests
from pydub import AudioSegment
import os

# initialize recognizer
r = sr.Recognizer()

# open the audio file using pydub
audio = AudioSegment.from_file("Audio_lecture.wav", format="wav")

# break the audio into chunks of 30 seconds each
chunk_length_ms = 30000
chunks = [audio[i:i+chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]

# loop through the chunks and recognize speech in each one
for i, chunk in enumerate(chunks):
    # export the chunk to a WAV file
    chunk.export("chunk{0}.wav".format(i), format="wav")

    # recognize the speech in the chunk
    with sr.AudioFile("chunk{0}.wav".format(i)) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data, language='ru-RU')
        print(text)

        # save the text to a file
        with open("recognized_text.txt", "a") as file:
            file.write(text)

    # delete the temporary WAV file
    os.remove("chunk{0}.wav".format(i))