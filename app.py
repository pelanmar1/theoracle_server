from flask import Flask, render_template, request, jsonify
import pandas
import os
import md5

UPLOAD_FOLDER = 'inputFiles'
ALLOWED_EXTENSIONS = set(['csv'])

inputFolder = 'inputFiles'
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
    done = False
    msg = ""
    if os.path.isfile(modelsFolder+'/'+rid+'.csv'):
        done = True
        msg = 'Job is complete'
    elif os.path.isfile(inputFolder+'/'+rid+'.csv'):
        msg = 'Job is in queue'
    else:
        msg = 'Job does not exist'
    return (done, msg)

@app.route('/status/<string:rid>')
def handleRequest(rid):
    (done, msg) = getReqStatus(rid)
    jsonDict = {'done': done, 'message':msg}
    return jsonify(jsonDict)

def getModels(rid):
    (done, msg) = getReqStatus(rid)
    if done:
	return pandas.read_csv(modelsFolder+'/'+rid+'.csv')
    else:
        return None

@app.route('/getmodels/<string:rid>')
def handleModelsRequest(rid):
    df = getModels(rid)
    if df:
        jsonDict = df.to_dict()
        return jsonify(jsonDict)
    else:
        return jsonify({'Message':'Models not ready or don\'t exist, check with /status/<rid>'})

def predict(rid, mid, df):
    return pandas.DataFrame()

@app.route('/predict/<string:rid>/<string:mid>', methods=['POST'])
def handlePredictRequest(rid, mid):
    file = request.files['file']
    file.save('tempFiles/'+file.filename)
    input_df = pandas.read_csv('tempFiles/'+file.filename)
    output_df = predict(rid, mid, input_df)
    jsonDict = output_df.to_dict()
    return jsonify(jsonDict)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

