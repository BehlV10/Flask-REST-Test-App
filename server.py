from flask import Flask, request, jsonify
import argparse
import sys
import csv
import json
import operator
import os.path

#Web app
app = Flask(__name__)

def getCSV():
    '''
    Get CSV file as a list
    '''
    data=[]
    csvfile = sys.argv[2]
    fields = ("ID","First","Last","Age","GithubAcct","Date of 3rd Grade Graduation")
    reader = csv.DictReader( open(csvfile), fieldnames=fields)
    next(reader) #Skip Header
    for row in reader:
        data.append(row)
    rows = list(reader)
    return data

@app.route('/ping',methods=['GET']) 
def pingServer():
    '''
    Ping request to make sure server is alive, return 'pong'
    '''
    return "pong"

@app.route('/people',methods=['GET'])
def getPeople():
    '''
    Return a standard JSON block of people in any order of format. Must be valid JSON
    '''
    people = getCSV()
    return jsonify(people)

@app.route('/people/age',methods=['GET'])
def sortPeopleByAge():
    '''
    Returns Json block containing a list of people sorted by age youngest to oldest
   '''
    fname = "output.json"
    if os.path.isfile(fname):
        people = json.load(open(fname))
    else:
        people = getCSV()
    people.sort(key=operator.itemgetter('Age'))
    lines = jsonify(people)
    return lines
    
@app.route('/ids/lastname/<lastname>',methods=['GET'])
def getIdsByLastName(lastname):
    '''
    Returns Json block of ids found for the given last name
    Using path params
    '''
    specified = []
    fname = "output.json"
    if os.path.isfile(fname):
        people = json.load(open(fname))
    else:
        people = getCSV()
    for person in people:
        if person['Last'] == lastname:
            specified.append(person['ID'])
    people = list(specified)
    lines = jsonify(people)
    return lines

@app.route('/update', methods=['GET', 'POST']) #allow both GET and POST requests
def updateData():
    '''
    Add data to JSON and save in a file. If file exists, use it over default CSV data
    '''
    if request.method == 'POST': #this block is only entered when the form is submitted
        id = request.form.get('id')
        first = request.form.get('first')
        last = request.form.get('last')
        age = request.form.get('age')
        github = request.form.get('github')
        graduation = request.form.get('github')
        fname = "output.json"
        if os.path.isfile(fname):
            people = json.load(open(fname))
        else:
            people = getCSV()
        new_person = ({
            "ID":id,
            "First":first,
            "Last":last,
            "Age":age,
            "GithubAcct":github,
            "Date of 3rd Grade Graduation":graduation
            })
        people.append(new_person)
        with open('output.json', 'w') as f:
            json.dump(people, f)
        lines = jsonify(people)
        return lines    
    
    return '''<form method="POST">
                  ID: <input type="number" name="id"><br>
                  First Name: <input type="text" name="first"><br>
                  Last Name: <input type="text" name="last"><br>
                  Age: <input type="number" name="age"><br>
                  Github Account: <input type="text" name="github"><br>
                  Date of 3rd Grade Graduation: <input type="text" name="graduation"><br>
                  <input type="submit" value="Submit"><br>
              </form>'''

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--debug", help="Optional Debug Mode for stack traces", action="store_true")
    parser.add_argument("port", help="Port number to run on")
    parser.add_argument("file", help="File to import data from")
    args = parser.parse_args()
    app.debug=args.debug
    app.run(host='localhost', port=int(sys.argv[1]))

