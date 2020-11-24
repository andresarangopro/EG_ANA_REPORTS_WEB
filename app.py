from flask import Flask, jsonify,request,render_template,send_file
import requests
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage




app = Flask(__name__,template_folder='templates')

app.config['UPLOAD_FOLDER'] = './reportes'

encargado = ['Andres Arango','Camilo Sanmartin','Santiago Castaneda','Juan Bernardo','Pepito perez']


@app.route('/listarReportes',methods=['GET'])
def listarReporte():
    reportes = requests.get('http://127.0.0.1:5100/reporte').json()
    return render_template('listarReporte.html',reportes=reportes)

@app.route('/crearReportes',methods=['GET'])
def crearReporte():
    return render_template('crearReporte.html',encargado=encargado)

@app.route('/download/<string:file>')
def downloadFile (file):
    path = "reportes/"+file
    return send_file(path, as_attachment=True)

@app.route("/guardarReporte",methods=['POST'])
def guardarReporte():
    reporte = dict(request.values)
    archivo = request.files['archivoDir']
    nombre = secure_filename(archivo.filename)
    archivo.save(os.path.join(app.config['UPLOAD_FOLDER'],nombre))
    rutaReporte = '../reportes/'+nombre
    reporte['archivoDir'] = rutaReporte
    reporte['estado'] = 'Pendiente'
    reporte['resultadoDir'] = nombre
    requests.post('http://127.0.0.1:5100/reporte',json=reporte)
    return(listarReporte())

app.run(port=8000,debug=True)