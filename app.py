from flask import Flask, request, jsonify

from database.db import initialize_db, db
from database.models import Category, Product
from database.schemas import ProductSchema, CategorySchema

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db and marshmallow
initialize_db(app)

# Create schemas
category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


# Getting the list of all categories
@app.route('/categories', methods=['GET'])
def get_categories():
    all_categories = Category.query.all()
    result = categories_schema.dump(all_categories)

    return jsonify(result)


# Getting the list of products of the concrete category
@app.route('/categories/<id>/products', methods=['GET'])
def get_category(id):
    category = Category.query.get(id)

    category_products = Product.query.with_parent(category).all()
    return products_schema.jsonify(category_products)


# Category CRUD
@app.route('/categories', methods=['POST'])
def add_category():
    try:
        name = request.json['name']

        new_category = Category(name)

        db.session.add(new_category)
        db.session.commit()
    except IntegrityError:
        return jsonify({'message': 'This category already exist'})
    return category_schema.jsonify(new_category)


@app.route('/categories/<id>', methods=['GET', 'PUT', 'DELETE'])
def category_handler(id):
    category = Category.query.get(id)

    try:
        if request.method == 'PUT':
            name = request.json['name']

            category.name = name

            db.session.commit()

            return category_schema.jsonify(category)

        elif request.method == 'DELETE':
            db.session.delete(category)
            db.session.commit()

            return category_schema.jsonify(category)
        else:
            return category_schema.jsonify(category)

    except AttributeError:
        return jsonify({"InternalServerError": {
            "message": "Something went wrong",
            "status": 500
        }})
    except UnmappedInstanceError:
        return jsonify({"UnmappedInstanceError": {
            "message": "Category does not exist",
            "status": 404
        }})


# Product CRUD
@app.route('/products', methods=['POST'])
def add_product():
    try:
        name = request.json['name']
        comment = request.json['comment']
        price = request.json['price']
        category_id = request.json['category_id']

        new_product = Product(name, comment, price, category_id)

        db.session.add(new_product)
        db.session.commit()
    except IntegrityError:
        return jsonify({'IntegrityError': {
            'message': 'This product already exist',
            'status': 400
        }})
    except:
        return jsonify({'InternalServerError': {
            'message': 'Something went wrong',
            'status': 500
        }})
    return product_schema.jsonify(new_product)


@app.route('/products/<id>', methods=['GET', 'PUT', 'DELETE'])
def product_handler(id):
    product = Product.query.get(id)

    try:
        if request.method == 'PUT':
            name = request.json['name']
            comment = request.json['comment']
            price = request.json['price']
            category_id = request.json['category_id']

            product.name = name
            product.comment = comment
            product.price = price
            product.category_id = category_id

            db.session.commit()

            return product_schema.jsonify(product)

        elif request.method == 'DELETE':
            db.session.delete(product)
            db.session.commit()

            return product_schema.jsonify(product)

        else:
            return product_schema.jsonify(product)

    except AttributeError:
        return jsonify({"InternalServerError": {
            "message": "Something went wrong",
            "status": 500
        }})
    except UnmappedInstanceError:
        return jsonify({"UnmappedInstanceError": {
            "message": "Product does not exist",
            "status": 404
        }})


if __name__ == '__main__':
    app.run(debug=True)
