import os, csv
from flask import Flask, render_template, request, send_from_directory
from werkzeug import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'tmp/'
app.config['ALLOWED_EXTENSIONS'] = set(['csv', 'html'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def file_proc():
    csvfile  = open('testes.csv', "rb")
    reader = csv.reader(csvfile)
    print reader[1]

    return 'Colunas disponiveis: ' + reader[1], 200

@app.route('/')
def index():
    formatsmsg = 'Only accept: '
    for x in app.config['ALLOWED_EXTENSIONS']:
        formatsmsg += ' ' + x.upper()
    return render_template('index.html', formatsmsg=formatsmsg)

@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return file_proc()
    else:
        return render_template('index.html', formatsmsg='Format not suported! Try again!')

app.run(debug=True, use_reloader=True)
