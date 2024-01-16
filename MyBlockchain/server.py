from flask import Flask, render_template, request
import sys
sys.path.append('/root/APathThroughDust')#替换为项目的实际根目录的绝对地址
from util.transaction import Necessary, Travel, Event


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('addTravel.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=50002)