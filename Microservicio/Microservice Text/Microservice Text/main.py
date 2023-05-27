from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('menu.html')



app.run(host='localhost',port=5000)