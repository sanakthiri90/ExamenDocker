import requests
from flask import Flask, jsonify, request, url_for
import json

import librosa 
import numpy as np
import pickle
import base64


app = Flask(__name__)
  
clf=pickle.load(open('model.pkl','rb'))

def getPrediction(soundfile):
	hop_length = 512
	n_fft = 2048
	n_mels = 128

	types = {0: 'blues', 1: 'classical', 2: 'country', 3: 'disco', 4: 'hiphop', 5: 'jazz', 6: 'metal', 7: 'pop', 8: 'reggae', 9: 'rock'}   
	print("test sanaaaa 11")
	#fich = soundfile["key"].decode("utf-8")	
	#decode_string = base64.b64decode(fich.encode("utf-8"))
	
		
	signal, rate = librosa.load(soundfile)  
	
	#The Mel Spectrogram
	S = librosa.feature.melspectrogram(signal, sr=rate, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels)
	S_DB = librosa.power_to_db(S, ref=np.max)
	S_DB = S_DB.flatten()[:1200]
	y_pred = clf.predict([S_DB])[0]
	print("test sanaaaa")	
	return types[y_pred]  
	
	
@app.route("/api/", methods=["POST"])
def hello():
	print("test sanaaaa22")	
	data = request.get_json(force=True) 
	wav_file = open("temp.wav", "wb")
	var=data["key"]
	decode_string = base64.b64decode(var.encode("utf-8"))
	wav_file.write(decode_string)
	#fi = fich = open('blues.00077.wav', 'rb') 
	
	print(decode_string)
	y = getPrediction("temp.wav")
	
	return "<h1>succes {{ y }} </h1>" + y 

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
if __name__ == '__main__':
   app.run(debug=True, port=5052, host='0.0.0.0')
