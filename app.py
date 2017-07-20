from flask import Flask, render_template, request
import pandas
import os
import md5

UPLOAD_FOLDER = 'inputFiles'
ALLOWED_EXTENSIONS = set(['csv'])

modelsFolder = 'models'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Right now only checks extension but can be edited to check any number of things abour the file to validate it
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Saves job file to specified location
def enqueueJob(df):
    rid=md5.md5(str(df)).hexdigest()
    df.to_csv('inputFiles/'+rid+'.csv')
    return rid

@app.route('/')
def dataForm():
    return render_template("dataForm.html")

@app.route('/', methods=['GET','POST'])
def handlePost():
    if request.method == 'POST':
        file = request.files['file']
	if file and allowed_file(file.filename):
	    file.save('tempFiles/'+file.filename)
	    df = pandas.read_csv('tempFiles/'+file.filename)
	    rid = enqueueJob(df)
            return rid + '\n'
	    #rid = md5.md5(str(file.read())).hexdigest()
	    #filename = rid+os.path.splitext(file.filename)[1] #[1] is the extension of the file
	    #file.stream.seek(0) # Go back to the start of the file
	    #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return filename+'\n'

    return "not ok"

def getReqStatus(rid):
    return (False, 'Ok') 

@app.route('/status/<string:rid>', methods=['GET'])
def handleRequest():
    return rid
    #(done, msg) = getReqStatus(rid)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

