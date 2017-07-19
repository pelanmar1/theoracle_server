from flask import Flask, render_template, request
import os
import md5

UPLOAD_FOLDER = 'inputFiles'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def dataForm():
    return render_template("dataForm.html")

@app.route('/', methods=['GET','POST'])
def handlePost():
    if request.method == 'POST':
        file = request.files['file']
	if file and allowed_file(file.filename):
	    rid = md5.md5(str(file.read())).hexdigest()
	    filename = rid+os.path.splitext(file.filename)[1] #[1] is the extension of the file
	    file.stream.seek(0) # Go back to the start of the file
	    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return filename+'\n'
	    #return "Ok"

    return "not ok"

    #x_in = request.form['xData']
    #y_in = request.form['yData']
    
    #csvFile = request.form['fileBtn']
    #return csvFile
    #df = pd.read_csv(csvFile)
    #return "Ok"
    #print(df)
    
    #data = {'x':[1,2,3]}
    #return """
    #<html>
    #    <head>
    #        <title>Prediction Service</title>
    #    </head>
    #    <body>
    #        <h1>Subtitle</h1>
    #	</body>
    #</html>"""
    #return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

