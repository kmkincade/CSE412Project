from __future__ import print_function # In python 2.7
import sys
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

@index.route('/insert')
def inserting():
    return render_template ('insertData.html')

@index.route('/debug')
def testing():
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("SELECT * from species")
		data = cursor.fetchall()
		if data is None:
			return "No species found"
		else:
			print(data, file=sys.stderr)
			return str(data)
	except Exception as e:
		print(e, file=sys.stderr)
		return str(e)
	finally:
		cursor.close() 
		conn.close()

#html to python from the insert buttons

@index.route('/insertResult', methods = ['POST'])
def insertResult():
    #if the button to insert a habitat is pushed, do stuff
    if 'insertHabitat' in request.form:
        habitatBiome = request.form['habitatBiome']
        habitatCountry = request.form['habitatCountry']
        habitatID = request.form['habitatID']
        resultStuff = 'The habitat with biome ' + habitatBiome + ' and country ' + habitatCountry + ' has been sent to the database.'
        insertHabitatQuery = 'INSERT INTO habitat(Biome, Country, HabitatID) VALUES(%s, %s, %s)'
		#send data to the database
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(insertHabitatQuery,(habitatBiome, habitatCountry, habitatCountry))
        except Exception as e:
            print(e, file=sys.stderr)
            resultStuff = 'There was an error with executing your query'
        finally:
            cursor.close() 
            conn.close()
		    #end send data to the database
            return render_template('resultsTest.html', result_stuff=resultStuff)
	#if the button to insert a species is pushed, do stuff
    elif 'insertSpecies' in request.form:
        return render_template('resultsTest.html', result_stuff = 'You created a new species.')
    else:
        return render_template('resultsTest.html', result_stuff = 'There was an error')
#end html to python


if __name__ == '__main__':
   index.run(debug = True, port = 8080)
