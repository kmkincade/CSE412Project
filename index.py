from __future__ import print_function # In python 2.7
import sys
from flask import Flask, render_template, request, redirect, url_for
#from flask_table import Table
from flaskext.mysql import MySQL

mysql = MySQL()

index = Flask(__name__)

# Uncomment and replace w/ remote DB for prod
index.config['MYSQL_DATABASE_USER'] = 'lmr6l4s7lv65y4vr'
index.config['MYSQL_DATABASE_PASSWORD'] = 'axe19y4ogn4rt55b'
index.config['MYSQL_DATABASE_DB'] = 'r88t2axx9fbpqxb9'
index.config['MYSQL_DATABASE_HOST'] = 'y06qcehxdtkegbeb.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
mysql.init_app(index)

@index.route('/')
def home_page():
    return render_template('searchOptions.html')

@index.route('/result', methods = ['GET'])
def searching():
    if 'SearchByCommonName' in request.values:
        _search = request.values['commonName']
        if request.values.get('speciesInfo'):
            try:
                conn = mysql.connect()
                cursor = conn.cursor()
                query = "SELECT * FROM species WHERE sName = '" + _search +"';"
                cursor.execute(query)
                data = cursor.fetchall()
                if data is None:
                    return "No species found"
                else:

                    return render_template('results.html', type = "Species",dataset = data)
            except Exception as e:
                print(e, file=sys.stderr)
                return str(e)
            finally:
                cursor.close()
                conn.close()
        elif request.values.get('relatedReading'):
            try:
                conn = mysql.connect()
                cursor = conn.cursor()
                query = "SELECT * FROM species WHERE sName = '" + _search +"';"
                cursor.execute(query)
                data = cursor.fetchall()
                if data is None:
                    return "No species found"
                else:

                    return render_template('results.html', type = "Species",dataset = data)
            except Exception as e:
                print(e, file=sys.stderr)
                return str(e)
            finally:
                cursor.close()
                conn.close()
        elif request.values.get('conservationInfo'):
            try:
                conn = mysql.connect()
                cursor = conn.cursor()
                query = "SELECT * FROM species WHERE sName = '" + _search +"';"
                cursor.execute(query)
                data = cursor.fetchall()
                if data is None:
                    return "No species found"
                else:

                    return render_template('results.html', type = "Species",dataset = data)
            except Exception as e:
                print(e, file=sys.stderr)
                return str(e)
            finally:
                cursor.close()
                conn.close()
        elif request.values.get('habitatInfo'):
            try:
                conn = mysql.connect()
                cursor = conn.cursor()
                query = "SELECT * FROM species WHERE sName = '" + _search +"';"
                cursor.execute(query)
                data = cursor.fetchall()
                if data is None:
                    return "No species found"
                else:

                    return render_template('results.html', type = "Species",dataset = data)
            except Exception as e:
                print(e, file=sys.stderr)
                return str(e)
            finally:
                cursor.close()
                conn.close()
        elif request.values.get('habitatThreats'):
            try:
                conn = mysql.connect()
                cursor = conn.cursor()
                query = "SELECT * FROM species WHERE sName = '" + _search +"';"
                cursor.execute(query)
                data = cursor.fetchall()
                if data is None:
                    return "No species found"
                else:

                    return render_template('results.html', type = "Species",dataset = data)
            except Exception as e:
                print(e, file=sys.stderr)
                return str(e)
            finally:
                cursor.close()
                conn.close()
    else:
        return render_template('results.html', dataset = request.values)


@index.route('/insert')
def inserting():
    return render_template('insertData.html')

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
    #print(request.form)
    if 'insertHabitat' in request.form:
        habitatBiome = str(request.form['habitatBiome'])
        habitatCountry = str(request.form['habitatCountry'])
        habitatID = str(request.form['habitatID'])
        resultStuff = 'The habitat with biome ' + habitatBiome + ' and country ' + habitatCountry + ' has been sent to the database.'

        isSafe = checkSafety(resultStuff)
        if isSafe == True:
            insertHabitatQuery = """INSERT INTO habitat (Biome, Country, HabitatID) VALUES('%s', '%s', '%s')""" % ((habitatBiome, habitatCountry, habitatCountry))
        else:
            insertHabitatQuery = "";
            resultStuff = "Invalid input!"
		#send data to the database
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            if insertHabitatQuery != "":
                print(insertSpeciesQuery)
                cursor.execute(insertHabitatQuery)
                conn.commit()
        except Exception as e:
            print(e, file=sys.stderr)
            resultStuff = 'There was an error with executing your query'
        finally:
            cursor.close() 
            conn.close()
		    #end send data to the database
            return render_template('resultsTest.html', result_stuff=resultStuff)
    elif 'insertSpecies' in request.form: #if the button to insert a species is pushed, do stuff
        speciesName = str(request.form['speciesName'])
        speciesTaxon = str(request.form['speciesTaxon'])
        speciesStatus = str(request.form['speciesStatus'])
        speciesPopulation = str(request.form['speciesPopulation'])

        resultStuff = 'You inserted a new species: ' + speciesName + ', ' + speciesTaxon + ', ' + speciesStatus + ', ' + speciesPopulation + '.'
        isSafe = checkSafety(resultStuff)
        if isSafe == True:
            insertSpeciesQuery = """INSERT INTO species (sName, Taxon, Sstatus, Population) VALUES('%s', '%s', '%s', '%s')""" %(speciesName, speciesTaxon, speciesStatus, speciesPopulation)
        else:
            insertSpeciesQuery = "";
            resultStuff = "Invalid input!"
		#send data to the database
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            if insertSpeciesQuery != "":
                print(insertSpeciesQuery)
                cursor.execute(insertSpeciesQuery)
                conn.commit()
        except Exception as e:
            print(e, file=sys.stderr)
            resultStuff = 'There was an error with executing your query'
        finally:
            cursor.close() 
            conn.close()
		    #end send data to the database
            return render_template('resultsTest.html', result_stuff=resultStuff)
        return render_template('resultsTest.html', result_stuff)
    else:
        return render_template('resultsTest.html', result_stuff = "There was an error. Most likely the form did not match.")
#end html to python

#sanitize input
def checkSafety(form):
    aString = str(form)
    if "drop" in aString.lower() or ";" in aString or "alter table" in aString.lower():
        return False;
    else:
        return True;
		
#end sanitize input


if __name__ == '__main__':
   index.run(debug = True, port = 8080)
