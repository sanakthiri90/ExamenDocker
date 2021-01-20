from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import librosa.display
import librosa 
import numpy as np
import pickle
#import base64


app = Flask(__name__)

clf=pickle.load(open('model.pkl','rb'))


def getPrediction(soundfile):
	hop_length = 512
	n_fft = 2048
	n_mels = 128

	types = {0: 'blues', 1: 'classical', 2: 'country', 3: 'disco', 4: 'hiphop', 5: 'jazz', 6: 'metal', 7: 'pop', 8: 'reggae', 9: 'rock'}   

	#decode_string = base64.b64decode(open(soundfile, "rb").read()).decode('utf-8')
	
	signal, rate = librosa.load(soundfile)  
	
	#The Mel Spectrogram
	S = librosa.feature.melspectrogram(signal, sr=rate, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels)
	S_DB = librosa.power_to_db(S, ref=np.max)
	S_DB = S_DB.flatten()[:1200]
	y_pred = clf.predict([S_DB])[0]
	
	return types[y_pred]

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/uploader', methods=['POST'])
def upload_file():
	if request.method == 'POST':
		f = request.files['file']
		f.save(secure_filename(f.filename))
		base64_str = base64.b64encode(open(f.filename, "rb").read())
		#base64_str = base64_str.decode('ascii')
		#base64_str = base64_str.decode("utf-8")
		y = getPrediction(f.filename)
		#print(base64_str)
	return "<h1>succes {{ y }} </h1>" + y 

if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0')


