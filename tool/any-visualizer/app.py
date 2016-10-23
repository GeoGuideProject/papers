import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os, csv, re
from flask import Flask, render_template, request, send_from_directory
from werkzeug import secure_filename

app = Flask(__name__)

# Directories config
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_TMP = os.path.join(APP_ROOT, 'tmp')
APP_ANALYSIS = os.path.join(APP_ROOT, 'dataanalysis')
app.config['UPLOAD_FOLDER'] = 'tmp/'
app.config['ALLOWED_EXTENSIONS'] = set(['csv'])

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
def dataanalysis():
    print("data analysis")
    return send_from_directory(APP_ANALYSIS, 'index.html')
def file_proc():
    examplevalues = []
    options = []
    mapsoptions = []
    with open(os.path.join(APP_TMP, 'arquivo.csv')) as f:
        firstline = True
        for row in csv.reader(iter(f.readline, '')):
            if(firstline == True):
                tempoptions = row
                firstline = False
            else:
                examplevalues = row
                break
    #Select numeric fields and add to options list
    for index, value in enumerate(examplevalues):
        try:
            float(value)
            options.append(tempoptions[index])
        except:
            None
    #Select in options list the possible values for lat and long, if not found show all int values
    for index, value in enumerate(tempoptions):
        if(value.find("lat") != -1):
            mapsoptions.append(tempoptions[index])
        elif(value.find("long") != -1):
            mapsoptions.append(tempoptions[index])
    if(len(mapsoptions) < 2):
        mapsoptions = []
        for index, value in enumerate(examplevalues):
            try:
                value = float(value)
                try:
                    int(value)
                except:
                    mapsoptions.append(tempoptions[index])
            except:
                None
    if(len(mapsoptions) < 2):
        mapsoptions = options

    maptoptionsreverse = mapsoptions[::-1]
    return render_template('select.html', option_list=options, mapsoptions=mapsoptions, mapsoptionsreverse=maptoptionsreverse)

@app.route('/')
def index():
    formatsmsg = 'Only accept: '
    for x in app.config['ALLOWED_EXTENSIONS']:
        formatsmsg += ' ' + x.upper()
    return render_template('index.html', formatsmsg=formatsmsg)

@app.route('/selectdata', methods=['POST'])
def selectdata():
    filter = [request.form.get('filter1'), request.form.get('filter2'),request.form.get('filter3'), request.form.get('filter4')]
    positions = [request.form.get('latitude1'),  request.form.get('longitude1'),  request.form.get('latitude2'),  request.form.get('longitude2')]
    return render_template('charts.html', csvfilename='arquivo.csv', filter=filter, positions=positions)

@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'arquivo.csv'))
        if(request.form.get('botao') == "Charts and Maps"):
            return file_proc()
        else:
            return dataanalysis()
    else:
        return render_template('index.html', formatsmsg='Format not suported! Try again!')

@app.route('/tmp/<path:filename>')
def sendcsv(filename):
    return send_from_directory(APP_TMP, filename)
@app.route('/dataanalysis/<path:filename>')
def sendinfos(filename):
    return send_from_directory(APP_ANALYSIS, filename)
@app.route('/static/<path:filename>')
def sendstatic(filename):
    return send_from_directory('/static', filename)

app.run(use_reloader=True, port=8090)
