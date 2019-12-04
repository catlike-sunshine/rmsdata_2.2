import base64
import datetime
import json
import os
import wave
import requests
#from pyaudio import PyAudio, paInt16
#from pydub import AudioSegment

# 获取token
def get_access_token():

	API_Key = 'MnWxNBSpaTQDZF4vRG4tus0N' # 换成你自己的

	Secret_Key = '959A6KFqg5RWlVE8VE0W7oa89BZwux3m' # 换成你自己的

	url = 'https://openapi.baidu.com/oauth/2.0/token?'

	payload = {
    	"grant_type": "client_credentials",
    	"client_id": API_Key,
    	"client_secret": Secret_Key
	}

	response = requests.get(url, params=payload, timeout=3)
	json_str = json.loads(response.text)

	access_token = json_str['access_token']

	return access_token


framerate = 16000
NUM_SAMPLES = 2000
channels = 1
sampwidth = 2
TIME = 2

## 前端传来的语音文件写入方式
#def save_wave_file(filename, data):
#
#	wf = wave.open(filename, 'wb')
#	wf.setnchannels(channels)
#	wf.setsampwidth(sampwidth)
#	wf.setframerate(framerate)
#	wf.writeframes(b"".join(data))
#	wf.close()


## 音频格式转换（mp3转wav）
#def trans_mp3_to_wav(filename):
#
#	# 转换前的语音地址
#	song = AudioSegment.from_mp3(filename)
#
#	# 转换后的语音地址
#	song.export(os.path.join(filename[:-3],wav),format="wav")


# 百度音频转换接口
def get_word(filename):

#	# 音频文件写入到服务器
#	save_wave_file(file_name, get_vido)


#	# 判断是否是mp3格式，若是则将音频为mp3格式转为wav格式
#    if filename[-3:] == "mp3":
#        trans_mp3_to_wav(filename)
    

	with open(filename, "rb") as f:
		speech = base64.b64encode(f.read()).decode('utf8')
    
	size = os.path.getsize(filename)

	headers = {'Content-Type': 'application/json'}

	access_token = get_access_token()

	url = 'https://vop.baidu.com/pro_api'
	data = {
    	"format": "wav",
    	"rate": 16000,
    	"channel": 1,
    	"cuid": 'zhichacha',
    	"dev_pid": 80001,
    	"token": access_token,
    	"len": size,
    	"speech": speech,

	}
	req = requests.post(url, json.dumps(data), headers)
	result = json.loads(req.text)

	return result


## 录音（微信小程序开发腾讯有录音功能所以这个没用上）
#def my_record():
#	pa = PyAudio()
#	stream = pa.open(format=paInt16, channels=1,
#                 	rate=framerate, input=True,
#                 	frames_per_buffer=NUM_SAMPLES)
#	my_buf = []
#	count = 0
#	# print('.')
#	# 控制录音时间
#	while count < TIME * 10:
#    	string_audio_data = stream.read(NUM_SAMPLES)
#    	my_buf.append(string_audio_data)
#    	count += 1
#
#	save_wave_file('01.wav', my_buf)
#	stream.close()