from flask import Flask, request, render_template

import requests
import os

MODEL_ART_API = os.getenv('MODEL_ART_API')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/carton/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return 'No file uploaded.', 400
    
    file = request.files['image']
    if file.filename == '':
        return 'Filename is empty.', 400

    resp = model_art_pic_carton(file)

    print(resp)
    return resp.json()

def model_art_pic_carton(file):
    payload = {}
    files=[ ('images',(file.filename,file,'image/png'))]
    headers = {
    'x-auth-token': get_token_from_fg_header()
    }
    response = requests.request("POST", MODEL_ART_API, headers=headers,
    data=payload, files=files,verify=False)
    return response

# 从FunctionGraph平台发送的请求里获取鉴权token
# 需要先配置委托 并且 在高级设置打开传入秘钥开关
def get_token_from_fg_header():
    return request.headers.get("X-Cff-Auth-Token")

if __name__ == '__main__':
    app.run(debug=True,port=8000,host="0.0.0.0")