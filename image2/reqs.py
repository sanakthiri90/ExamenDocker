import requests
import json

url = 'http://0.0.0.0:5052/api/'

data = "salut sana"
j_data = json.dumps(data)
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
r = requests.post(url, data=j_data, headers=headers)
print(r, r.text)






import requests
from flask import Flask, jsonify, request
import json

app = Flask(__name__)

  
#@app.route("/test", methods=["POST"])
#def test():
url = 'http://monimg2:5052/api/'

#r1 = requests.post(url,'')
#print(r1, r1.text)
	  


data = "salut sana"
j_data = json.dumps(data)
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
r = requests.post(url, data=j_data, headers=headers)
print(r, r.text)
	  
    

if __name__ == '__main__':
   app.run(debug=True, port=5000, host='0.0.0.0')
   
   
