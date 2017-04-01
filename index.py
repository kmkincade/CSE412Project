from flask import Flask, render_template
index = Flask(__name__)

@index.route('/')
def home_page():
   return render_template('home.html')

if __name__ == '__main__':
   index.run(debug = True, port = 8080)