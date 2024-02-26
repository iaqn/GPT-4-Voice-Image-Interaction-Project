#一共三块内容 1.语音转文本   2.文本+图片 转给api 返回结果  3.将结果里的content转成语音播放出来
#! 需要api的地方 54行 122行 要设置，不设置不能运行  68行也要设置
#! 注意变量mytext image_path text_to_speech
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os

#  下面是语音转文本的代码，mytext是识别后的文本内容  如果不需要语音的话，可以直接删了。
# Initialize the recognizer
recognizer = sr.Recognizer()

while True:
    try:
        # Start the microphone and begin recording
        with sr.Microphone() as source:
            print("Please speak now...")
            audio = recognizer.listen(source)

        # Use Google Web Speech API to convert audio to text
        mytext = recognizer.recognize_google(audio, language='zh-CN')
        print("You said: " + mytext)
        break  # Break the loop if successful

    except sr.UnknownValueError:
        text1 = "无法识别你所说的内容，请你再重新说一遍"
        print(text1)
        # Convert text to speech and play it
        tts = gTTS(text=text1, lang='zh-cn')
        temp_file1 = "temp1.mp3"
        tts.save(temp_file1)
        playsound(temp_file1)
        os.remove(temp_file1)

    except sr.RequestError as e:
        print(f"Could not request results from Google Web Speech API; {e}")
        text2 = "无法连接网络，请你再重新说一遍"
        # Convert text to speech and play it
        tts = gTTS(text=text2, lang='zh-cn')
        temp_file2 = "temp2.mp3"
        tts.save(temp_file2)
        playsound(temp_file2)
        os.remove(temp_file2)





#下面是把mytext和图片所在的地址image_path 一起给gpt4-api 得到内容 text_to_speech




mykey='xxx' #!这里需要设置自己的gpt4-api-key  注意必须是gpt-4-vision-preview 的api，其他的模型没有图片识别功能（我没试过）

import base64
import requests

# OpenAI API Key
api_key = mykey

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "images/1.jpg" #! 这里是读取图片的路径，要改一下

# Getting the base64 string
base64_image = encode_image(image_path)

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

payload = {
  "model": "gpt-4-vision-preview",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": mytext  #!这里就是上面语音转文本的变量
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          }
        }
      ]
    }
  ],
  "max_tokens": 1500
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

print(response.json())


# 假设您已经有了 JSON 响应
response_json = response.json()

# 提取 'content'
text_to_speech = response_json['choices'][0]['message']['content']
print(text_to_speech)


#以下是将内容text_to_speech转成语音播放的代码



from openai import OpenAI
from pathlib import Path
from pydub import AudioSegment
from pydub.playback import play
import io
client = OpenAI(api_key="xxx") #! 这里的api-key 跟上面的是同一个(也可以不是同一个，我只是为了省力一点)，gpt-4-vision-preview 的api 也可以运用到tts-1模型上，我尝试过google的免费文本转语音模型，发现效果不太好，还是氪金最有用
def text_to_speech_openai(text, voice='nova'):
    try:
        # 使用 OpenAI 的 TTS 模型
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )

        # 将音频数据转换为可播放的格式
        audio_data = response.content
        audio_stream = io.BytesIO(audio_data)
        audio = AudioSegment.from_file(audio_stream, format="mp3")

        # 播放音频
        play(audio)
    except Exception as e:
        print("播放语音失败，错误信息：", e)


# 调用函数
text_to_speech_openai(text_to_speech)


