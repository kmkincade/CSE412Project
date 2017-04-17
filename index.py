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

def getSymbolForFilter(filter):
    return {
        'greaterThan': ">",
        'lessThan': "<",
        'greaterThanOrEqual': ">=",
        'lessThanOrEqual': "<=",
        'equalTo': "="
    }[filter]


@index.route('/')
def home_page():
    return render_template('searchOptions.html')

@index.route('/result', methods = ['GET'])
def searching():
    print(request.values, file=sys.stderr)
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        speciesData = 0
        readingData = 0
        conservationData = 0
        habitatData = 0
        threatData = 0

        if 'SearchByCommonName' in request.values:
            _search = request.values['commonName']
            if request.values.get('speciesInfo'):
                query = "SELECT * FROM species WHERE sName = '" + _search +"';"
                cursor.execute(query)
                speciesData = cursor.fetchall()
            if request.values.get('relatedReading'):
                query = "SELECT R.* FROM species AS S, relatedReading AS R WHERE S.sName = '" + _search + "' AND R.Taxon = S.Taxon"
                cursor.execute(query)
                readingData = cursor.fetchall()
            if request.values.get('conservationInfo'):
                query = "SELECT H.Taxon, C.cName FROM species AS S, helpedBy AS H, conservation AS C WHERE S.sName = '" + _search + "' AND S.Taxon = H.Taxon AND C.ConservationID = H.ConservationID"
                cursor.execute(query)
                conservationData = cursor.fetchall()
            if request.values.get('habitatInfo'):
                query = "SELECT H.Biome, H.Country FROM species AS S, livesIn AS L, habitat AS H WHERE S.sName = '" + _search + "' AND S.Taxon = L.Taxon AND L.HabitatID = H.HabitatID"
                cursor.execute(query)
                habitatData = cursor.fetchall()
            if request.values.get('habitatThreats'):
                query = "SELECT DISTINCT T.tName FROM destroys AS D, threats AS T, habitat AS H, livesIn AS L, species AS S WHERE"
                query += " S.sName = '" + _search + "' AND S.Taxon = L.Taxon AND L.HabitatID = H.HabitatID AND D.HabitatID = H.HabitatID "
                query += "AND D.ThreatID = T.ThreatID"
                cursor.execute(query)
                threatData = cursor.fetchall()
            data = [{'columnNames': ["Common Name", "Taxon", "Status", "Population"], 'type': "Species", 'data' : speciesData }, {'columnNames':["URL", "Type", "Taxon"] , 'type': "Related Reading", 'data' : readingData},{'columnNames':["Taxon", "Conservation"] , 'type': "Conservation", 'data' : conservationData},{'columnNames':["Biome", "Country"] , 'type': "Habitat", 'data': habitatData},{'columnNames':["Threat Name"] , 'type': "Habitat Threats", 'data' : threatData} ]
            return render_template('results.html', dataset=data)
        elif 'Search By Species Name' in request.values:
                _search = request.values['speciesName']
                if request.values.get('speciesInfo'):
                    query = "SELECT * FROM species WHERE Taxon = '" + _search + "';"
                    cursor.execute(query)
                    speciesData = cursor.fetchall()
                if request.values.get('relatedReading'):
                    query = "SELECT R.* FROM species AS S, relatedReading AS R WHERE S.Taxon = '" + _search + "' AND R.Taxon = S.Taxon"
                    cursor.execute(query)
                    readingData = cursor.fetchall()
                if request.values.get('conservationInfo'):
                    query = "SELECT H.Taxon, C.cName FROM species AS S, helpedBy AS H, conservation AS C WHERE S.Taxon = '" + _search + "' AND S.Taxon = H.Taxon AND C.ConservationID = H.ConservationID"
                    cursor.execute(query)
                    conservationData = cursor.fetchall()
                if request.values.get('habitatInfo'):
                    query = "SELECT H.Biome, H.Country FROM species AS S, livesIn AS L, habitat AS H WHERE S.Taxon = '" + _search + "' AND S.Taxon = L.Taxon AND L.HabitatID = H.HabitatID"
                    cursor.execute(query)
                    habitatData = cursor.fetchall()
                if request.values.get('habitatThreats'):
                    query = "SELECT DISTINCT T.tName FROM destroys AS D, threats AS T, habitat AS H, livesIn AS L, species AS S WHERE"
                    query += " S.Taxon = '" + _search + "' AND S.Taxon = L.Taxon AND L.HabitatID = H.HabitatID AND D.HabitatID = H.HabitatID "
                    query += "AND D.ThreatID = T.ThreatID"
                    cursor.execute(query)
                    threatData = cursor.fetchall()
                data = [{'columnNames': ["Common Name", "Taxon", "Status", "Population"], 'type': "Species",'data': speciesData},
                        {'columnNames': ["URL", "Type", "Taxon"], 'type': "Related Reading", 'data': readingData},
                        {'columnNames': ["Taxon", "Conservation"], 'type': "Conservation", 'data': conservationData},
                        {'columnNames': ["Biome", "Country"], 'type': "Habitat", 'data': habitatData},
                        {'columnNames': ["Threat Name"], 'type': "Habitat Threats", 'data': threatData}]
                return render_template('results.html', dataset=data)
        elif 'belowAveragePopulation' in request.values:
            _status = request.values.get('status')
            print(_status, file=sys.stderr)
            if _status:
                query = ("SELECT * "
                "FROM species as s1 "
                "WHERE s1.sstatus = \"" + _status + "\" AND "
                "population < ( "
                    "SELECT AVG(population) "
                    "FROM species as s2 "
                    "WHERE s1.sstatus = s2.sstatus);")
                print(query, file=sys.stderr)
                cursor.execute(query)
                data = cursor.fetchall()
                if data is None:
                    return "No species found"
                else:
                    return render_template('results.html', type = "Species",dataset = data)
        elif 'speciesCount' in request.values:
            _filter = getSymbolForFilter(request.values.get('filter'))
            _speciesNum = request.values.get('speciesNum')
            print(_filter, file=sys.stderr)
            if _filter and _speciesNum:
                query = ("SELECT h.Biome, h.Country, COUNT(s.Taxon) as 'Species Count' "
                "FROM habitat as h, species as s, livesIn as li "
                "WHERE "
                "s.Taxon = li.Taxon AND "
                "h.HabitatID = li.HabitatID "
                "GROUP BY h.HabitatID "
                "HAVING COUNT(s.Taxon) "+ _filter +" " + _speciesNum + " ;"
                )
                cursor.execute(query)
                data = cursor.fetchall()
                print(data, file=sys.stderr)
                if data is None:
                    return "No biomes found"
                else:
                    return render_template('results.html', type = "Biome",dataset = data)
        else:
            return render_template('results.html', dataset = request.values)
    except Exception as e:
        print(e, file=sys.stderr)
        return str(e)
    finally:
        cursor.close()
        conn.close()


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
        speciesData = 0
        speciesData = 0
        readingData = 0
        conservationData = 0
        habitatData = 0
        threatData = 0
        habitatBiome = str(request.form['habitatBiome'])
        habitatCountry = str(request.form['habitatCountry'])
        habitatID = str(request.form['habitatID'])
        resultStuff = 'The habitat with biome ' + habitatBiome + ' and country ' + habitatCountry + ' has been inserted into the database.'

        isSafe = checkSafety(resultStuff)
        if isSafe == True:
            insertHabitatQuery = """INSERT INTO habitat (Biome, Country, HabitatID) VALUES('%s', '%s', '%s')""" % ((habitatBiome, habitatCountry, habitatID))
        else:
            insertHabitatQuery = "";
            resultStuff = "Invalid input!"
		#send data to the database
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            if insertHabitatQuery != "":
                print(insertHabitatQuery)
                cursor.execute(insertHabitatQuery)
                conn.commit()

                # now request the inserted species element to confirm it was added
                query = "SELECT h.Biome, h.Country, h.HabitatID FROM habitat h WHERE h.Biome = '" + habitatBiome + "'" + "AND h.Country = '" + habitatCountry + "' AND h.HabitatID = '" + habitatID + "'"
                cursor.execute(query)
                habitatData = cursor.fetchall()

                if habitatData is None:
                    resultStuff = 'There was an error retrieving the data after insert.'
               # end request of inserted element
        except Exception as e:
            print(e, file=sys.stderr)
            if "Duplicate" in str(e):
                resultStuff = 'There already exists an entry for that primary key. Insert failed.'
            else:
                resultStuff = 'There was an error with executing your query'
        finally:
            cursor.close() 
            conn.close()
		    #end send data to the database
        data = [{'columnNames': ["Common Name", "Taxon", "Status", "Population"], 'type': "Species", 'data': speciesData},{'columnNames': ["URL", "Type", "Taxon"], 'type': "Related Reading", 'data': readingData},{'columnNames': ["Taxon", "Conservation"], 'type': "Conservation", 'data': conservationData},{'columnNames': ["Biome", "Country"], 'type': "Habitat", 'data': habitatData},{'columnNames': ["Threat Name"], 'type': "Habitat Threats", 'data': threatData}]
        return render_template('resultsTest.html', result_stuff=resultStuff, type="Habitat", dataset=data)
    elif 'insertSpecies' in request.form: #if the button to insert a species is pushed, do stuff
        # if the button to insert a species is pushed, do stuff
        speciesData = 0
        speciesData = 0
        readingData = 0
        conservationData = 0
        habitatData = 0
        threatData = 0
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
                # now request the inserted species element to confirm it was added
                query = "SELECT s.sName, s.Taxon, s.Sstatus, s.Population FROM species s WHERE s.Taxon = '" + speciesTaxon + "'" + "AND s.sName = '" + speciesName + "' AND s.Sstatus = '" + speciesStatus + "' AND s.Population = '" + speciesPopulation + "'"
                cursor.execute(query)
                speciesData = cursor.fetchall()
                if speciesData is None:
                    resultStuff = 'There was an error retrieving the data after insert.'
                # end request of inserted element
        except Exception as e:
            print(e, file=sys.stderr)
            if "Duplicate" in str(e):
                resultStuff = 'There already exists an entry for that primary key. Insert failed.'
            else:
                resultStuff = 'There was an error with executing your query'
        finally:
            cursor.close() 
            conn.close()
		    #end send data to the database
            data = [{'columnNames': ["Common Name", "Taxon", "Status", "Population"], 'type': "Species",'data': speciesData},{'columnNames': ["URL", "Type", "Taxon"], 'type': "Related Reading", 'data': readingData},{'columnNames': ["Taxon", "Conservation"], 'type': "Conservation", 'data': conservationData},{'columnNames': ["Biome", "Country"], 'type': "Habitat", 'data': habitatData},{'columnNames': ["Threat Name"], 'type': "Habitat Threats", 'data': threatData}]
            return render_template('resultsTest.html', result_stuff=resultStuff, type="Species", dataset=data)
    else:
        return render_template('resultsTest.html', result_stuff = "There was an error. Most likely the form did not match.")
#end html to python

#sanitize input
def checkSafety(form):
    aString = str(form)
    if "drop" in aString.upper().lower() or ";" in aString or "alter table" in aString.lower():
        return False;
    else:
        return True;
		
#end sanitize input


if __name__ == '__main__':
   index.run(debug = True, port = 8080)
