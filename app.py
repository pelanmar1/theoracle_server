from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
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
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

