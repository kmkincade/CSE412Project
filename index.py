from flask import Flask, render_template
from flaskext.mysql import MySQL

mysql = MySQL()

index = Flask(__name__)

# Uncomment and replace w/ remote DB for prod
# index.config['MYSQL_DATABASE_USER'] = 'root'
# index.config['MYSQL_DATABASE_PASSWORD'] = 'root'
# index.config['MYSQL_DATABASE_DB'] = 'dbName'
# index.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(index)

@index.route('/')
def home_page():
   return render_template('searchOptions.html')

if __name__ == '__main__':
   index.run(debug = True, port = 8080)