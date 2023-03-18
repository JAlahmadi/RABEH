import openai
import pyaudio
import wave
import requests
ss_api_key = "ff82e1ca5623cc89be1823c2617b7574795976af"
openai.api_key = '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'
model_id = 'whisper-1'
#------------------------------------------sound capture ----------------------------------------------------------
def rec():
    frames_buf = 3200
    format = pyaudio.paInt16
    CHANNELS =1
    RATE = 16000

    p= pyaudio.PyAudio()

    stream = p.open(
        format= format,
        channels= CHANNELS,
        rate= RATE,
        input= True,
        frames_per_buffer= frames_buf
    )

    print("start recording ....")

    sec = 5
    frames =[]
    for i in range(0, int(RATE/frames_buf*sec)):
        data = stream.read(frames_buf)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate
    print("end recording")
    obj = wave.open("output.wav", "wb")
    obj.setnchannels(CHANNELS)
    obj.setsampwidth(p.get_sample_size(format))
    obj.setframerate(RATE)
    obj.writeframes(b"".join(frames))
    obj.close()
#----------------------------------------------------------------------------------------------------
rec()


audio_file= open('output.wav', 'rb')
transcript = openai.Audio.translate(
    model= model_id,
    file=audio_file,
    response_format= 'text'
    )

print(transcript)

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": transcript},
    {"role": "user", "content": "can you get the company stock ticker?"}
  ]
)

print(completion.choices[-1].message.content)