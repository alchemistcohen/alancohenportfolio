from flask import Flask, render_template, request
from datetime import datetime, timedelta

app = Flask(__name__)

# Función para calcular la fecha de vencimiento y la fecha juliana a partir de la fecha de elaboración y la vida útil
def calcular_desde_elaboracion(fecha_elaboracion, vida_util):
    fecha_vencimiento = fecha_elaboracion + timedelta(days=vida_util)
    fecha_juliana = fecha_vencimiento.strftime('%j')
    return fecha_vencimiento, fecha_juliana

# Función para calcular la fecha de vencimiento y la fecha de elaboración a partir de la fecha juliana y la vida útil
def calcular_desde_juliana(fecha_juliana, vida_util):
    fecha_vencimiento = datetime.strptime(fecha_juliana, '%Y%j')
    fecha_elaboracion = fecha_vencimiento - timedelta(days=vida_util)
    return fecha_vencimiento, fecha_elaboracion

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    opcion = request.form['opcion']
    vida_util = int(request.form['vida_util'])
    
    if opcion == 'elaboracion':
        fecha_elaboracion_str = request.form['fecha_elaboracion']
        fecha_elaboracion = datetime.strptime(fecha_elaboracion_str, '%Y-%m-%d')
        fecha_vencimiento, fecha_juliana = calcular_desde_elaboracion(fecha_elaboracion, vida_util)
        return render_template('resultado.html', fecha_vencimiento=fecha_vencimiento.date(), fecha_juliana=fecha_juliana)

    elif opcion == 'juliana':
        fecha_juliana = request.form['fecha_juliana']
        fecha_vencimiento, fecha_elaboracion = calcular_desde_juliana(fecha_juliana, vida_util)
        return render_template('resultado.html', fecha_vencimiento=fecha_vencimiento.date(), fecha_elaboracion=fecha_elaboracion.date())

if __name__ == '__main__':
    app.run(debug=True)
