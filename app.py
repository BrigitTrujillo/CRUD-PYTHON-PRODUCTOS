from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect
from werkzeug.utils import secure_filename
import os
import uuid
from dotenv import load_dotenv
from pymongo import MongoClient
<<<<<<< HEAD
from bson.objectid import ObjectId
=======
>>>>>>> ed04d2dcc0b476724a71b3993f13adcf3f47b84a

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# Other configurations...

upload_folder = 'uploads'

if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

# MongoDB connection
<<<<<<< HEAD
client = MongoClient('mongodb+srv://brigittrujillo:12345@cluster0.tmcoio0.mongodb.net/productos?retryWrites=true&w=majority')

db = client.productos

=======
client = MongoClient(os.getenv('mongodb+srv://britrujillo:1234@cluster0.tmcoio0.mongodb.net/productos?retryWrites=true&w=majority'))
db = client.productos

>>>>>>> ed04d2dcc0b476724a71b3993f13adcf3f47b84a
app.secret_key = 'many random bytes'
app.config['UPLOAD_FOLDER'] = 'uploads'


@app.route('/productos')
def Index():
    data = db.productos.find()
<<<<<<< HEAD
    return render_template('index.html', productos=data)

=======
    return render_template('index.html', students=data)
>>>>>>> ed04d2dcc0b476724a71b3993f13adcf3f47b84a


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

<<<<<<< HEAD
        productos = {
=======
        product = {
>>>>>>> ed04d2dcc0b476724a71b3993f13adcf3f47b84a
            'nombre': nombre,
            'descripcion': descripcion,
            'precio': precio,
            'stock': stock,
            'imagen': filename
        }

<<<<<<< HEAD
        db.productos.insert_one(productos)
        return redirect(url_for('Index'))


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
=======
        db.productos.insert_one(product)
        return redirect(url_for('Index'))


@app.route('/delete/<int:id_data>', methods=['GET'])
def delete(id_data):
    product = db.productos.find_one({'_id': id_data})
    if product:
        filename = product['imagen']
        if filename:
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            except:
                flash('Error deleting the image file.')

        db.productos.delete_one({'_id': id_data})
>>>>>>> ed04d2dcc0b476724a71b3993f13adcf3f47b84a
        flash("Data Deleted Successfully")
    return redirect(url_for('Index'))


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
        return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(debug=True)
