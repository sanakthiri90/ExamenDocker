import requests
from flask import Flask, jsonify, request
import json
import base64


app = Flask(__name__)
  
@app.route("/test", methods=["POST"])
def test():
	url = 'http://0.0.0.0:5053/api/'
	
	fich = open('reggae.00010.wav', 'rb') 

	
	data_encode = base64.b64encode(fich.read())

	print(data_encode)
	
	headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
	#r = requests.post(url, data=base64_str, headers=headers)
	r = requests.post(url, json={"key": data_encode.decode("utf-8")}, headers=headers)
	
	print(r, r.text)
	return (r.text)
		  
    

if __name__ == '__main__':
   app.run(debug=True, port=5000, host='0.0.0.0', threaded=True)
   
   
