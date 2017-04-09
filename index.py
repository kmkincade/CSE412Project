from flask import Flask, render_template, request, redirect, url_for
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

@index.route('/result')
def searching():
    return render_template ('results.html')


#testing html to python interaction. Feel free to remove if this is causing issues.
@app.route('/habitatAdded', methods = ['POST'])
def habitatAdded():
    habitatBiome = request.form['habitatBiome']
    habitatCountry = request.form['habitatCountry']
    print("The habitat with biome " + habitatBiome + " and country " + habitatCountry + "has been sent to the database.")
    return redirect('/')
#end testing

if __name__ == '__main__':
   index.run(debug = True, port = 8080)
