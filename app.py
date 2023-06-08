from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.utils import secure_filename
import os
import uuid
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = 'many random bytes'
app.config['UPLOAD_FOLDER'] = 'uploads'

upload_folder = app.config['UPLOAD_FOLDER']

if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

# MongoDB connection
client = MongoClient('mongodb+srv://brigittrujillo:12345@cluster0.tmcoio0.mongodb.net/productos?retryWrites=true&w=majority')
db = client.productos

@app.route('/productos')
def index():
    data = db.productos.find()
    return render_template('index.html', productos=data)

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        stock = request.form['stock']

        imagen = request.files['imagen']
        if imagen:
            # Generate a unique name for the image
            filename = str(uuid.uuid4().hex) + secure_filename(imagen.filename)
            imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None

        product = {
            'nombre': nombre,
            'descripcion': descripcion,
            'precio': precio,
            'stock': stock,
            'imagen': filename
        }

        db.productos.insert_one(product)
        return redirect(url_for('index'))

@app.route('/delete/<string:id_data>', methods=['GET'])
def delete(id_data):
    # Convert id_data to ObjectId
    product_id = ObjectId(id_data)

    product = db.productos.find_one({'_id': product_id})
    if product:
        filename = product['imagen']
        if filename:
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            except:
                flash('Error deleting the image file.')

        db.productos.delete_one({'_id': product_id})
        flash("Data Deleted Successfully")
    return redirect(url_for('index'))

@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        id_data = int(request.form['id'])
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        stock = request.form['stock']

        imagen = request.files['imagen']
        if imagen:
            # Generate a unique name for the image
            filename = str(uuid.uuid4().hex) + secure_filename(imagen.filename)
            imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Update the image column in the database only if a new image is provided
            db.productos.update_one(
                {'_id': id_data},
                {'$set': {
                    'nombre': nombre,
                    'descripcion': descripcion,
                    'precio': precio,
                    'stock': stock,
                    'imagen': filename
                }}
            )
        else:
            # Keep the existing image in the database
            db.productos.update_one(
                {'_id': id_data},
                {'$set': {
                    'nombre': nombre,
                    'descripcion': descripcion,
                    'precio': precio,
                    'stock': stock
                }}
            )

        flash("Data Updated Successfully")
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
