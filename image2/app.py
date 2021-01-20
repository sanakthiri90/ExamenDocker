import requests
from flask import Flask, jsonify, request, url_for
import json

# Import the libraries
from sklearn import svm
from pycm import *
from os import walk
import librosa 
import numpy as np
import pickle
import base64
import os.path

app = Flask(__name__)
  


def extractMelSpectrogram_features(folder):
    hop_length = 512
    n_fft = 2048
    n_mels = 128
    
    labels = {'blues': 0, 'classical': 1, 'country': 2, 'disco': 3, 'hiphop': 4, 'jazz': 5, 'metal': 6, 'pop': 7, 'reggae': 8, 'rock': 9}
    a = []
    b = []
    for nametype in list(labels.keys()):
        _wavs = []
        wavs_duration = []
        for (_,_,filenames) in walk(folder+nametype+"/"):
            _wavs.extend(filenames)
            break
        Mel_Spectrogram = []
        for _wav in _wavs:
            # read audio samples
            if(".wav" in _wav): 
                file = folder +nametype+"/"+_wav
                print ("-"+file)
                signal, rate = librosa.load(file)  
                #The Mel Spectrogram
                S = librosa.feature.melspectrogram(signal, sr=rate, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels)
                S_DB = librosa.power_to_db(S, ref=np.max)
                #Mel_Spectrogram.append(S_DB)
                #print (S_DB)
                S_DB = S_DB.flatten()[:1200]
                a.append(S_DB)
                b.append(labels[nametype])
                
    return a, b

def getPrediction(soundfile,clf):
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

	#folder = "./Data/genres_original/"
	#a, b = extractMelSpectrogram_features(folder)

	#clf = svm.SVC()
	#clf = svm.SVC(kernel="rbf")
	#clf.fit(a,b)	

	modele='trainedmodel.sav'
	#pickle.dump(clf,open(modele,'wb'))
	
	#print(decode_string)
	#fl = "/home/user/Bureau/flask/image2/Data/genres_original/blues/blues.00004.wav"
	
	loaded_model=pickle.load(open(modele,'rb'))
	y = getPrediction("temp.wav",loaded_model)

	return "<h1>succes {{ y }} </h1>" + y 
	print(y)

		
		
if __name__ == '__main__':
   app.run(debug=True, port=5053, host='0.0.0.0')
