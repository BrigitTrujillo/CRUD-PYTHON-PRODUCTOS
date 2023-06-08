from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect
import boto3
from werkzeug.utils import secure_filename
import os
import uuid
from dotenv import load_dotenv

# Configuración de la conexión con DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# Obtener una referencia a la tabla en DynamoDB
table = dynamodb.Table('productos')

# Configuración de la conexión con RDS (MySQL)
# El código relacionado con MySQL se puede eliminar
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
            # Generar un nombre único para la imagen
            filename = str(uuid.uuid4().hex) + secure_filename(imagen.filename)
            imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None

        # Insertar los datos en DynamoDB
        item = {
            'nombre': nombre,
            'descripcion': descripcion,
            'precio': precio,
            'stock': stock,
            'imagen': filename
        }
        table.put_item(Item=item)

        return redirect(url_for('Index'))
@app.route('/delete/<int:id_data>', methods=['GET'])
def delete(id_data):
    # Obtener los detalles del producto antes de eliminarlo
    response = table.get_item(Key={'id': id_data})
    item = response.get('Item', None)
    if item:
        filename = item.get('imagen')
        if filename:
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            except:
                flash('Error deleting the image file.')

        # Eliminar el elemento de DynamoDB
        table.delete_item(Key={'id': id_data})
        flash("Data Deleted Successfully")
    else:
        flash("Product not found")

    return redirect(url_for('Index'))
@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        stock = request.form['stock']

        imagen = request.files['imagen']
        if imagen:
            # Generar un nombre único para la imagen
            filename = str(uuid.uuid4().hex) + secure_filename(imagen.filename)
            imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Actualizar la columna de imagen en DynamoDB solo si se proporciona una nueva imagen
            table.update_item(
                Key={'id': id_data},
                UpdateExpression='SET nombre = :nombre, descripcion = :descripcion, precio = :precio, stock = :stock, imagen = :imagen',
                ExpressionAttributeValues={
                    ':nombre': nombre,
                    ':descripcion': descripcion,
                    ':precio': precio,
                    ':stock': stock,
                    ':imagen': filename
                }
            )
        else:
            # Actualizar los campos sin cambiar la imagen en DynamoDB
            table.update_item(
                Key={'id': id_data},
                UpdateExpression='SET nombre = :nombre, descripcion = :descripcion, precio = :precio, stock = :stock',
                ExpressionAttributeValues={
                    ':nombre': nombre,
                    ':descripcion': descripcion,
                    ':precio': precio,
                    ':stock': stock
                }
            )

        flash("Data Updated Successfully")
        return redirect(url_for('Index'))
