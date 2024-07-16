from flask import Flask, request, jsonify, render_template, redirect, url_for
import redis
import json
from flasgger import Swagger, swag_from

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379, decode_responses=True)
swagger = Swagger(app)

@app.route('/')
def index():
    products = {k: json.loads(v) for k, v in r.hgetall('product').items()}
    return render_template('index.html', products=products)

@app.route('/product/<product_id>')
def get_product_page(product_id):
    product = r.hget('product', product_id)
    if product:
        return render_template('product.html', product=json.loads(product))
    return redirect(url_for('index'))

@app.route('/product', methods=['POST'])
def create_or_update_product():
    data = request.form.to_dict()
    product_id = data.get('id')
    r.hset('product', product_id, json.dumps(data))
    return redirect(url_for('index'))

@app.route('/product/delete/<product_id>', methods=['POST'])
def delete_product(product_id):
    r.hdel('product', product_id)
    return redirect(url_for('index'))

# API routes for JSON responses
@app.route('/api/products', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'A list of products',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'string'},
                        'name': {'type': 'string'},
                        'description': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def get_products():
    products = {k: json.loads(v) for k, v in r.hgetall('product').items()}
    return jsonify(products)

@app.route('/api/product/<product_id>', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'Product details',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'string'},
                    'name': {'type': 'string'},
                    'description': {'type': 'string'}
                }
            }
        },
        404: {
            'description': 'Product not found'
        }
    }
})
def get_product(product_id):
    product = r.hget('product', product_id)
    if product:
        return jsonify(json.loads(product)), 200
    return jsonify({'error': 'Product not found'}), 404

@app.route('/api/product', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'id',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'The product ID'
        },
        {
            'name': 'name',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'The product name'
        },
        {
            'name': 'description',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'The product description'
        }
    ],
    'responses': {
        200: {
            'description': 'Product created/updated successfully'
        }
    }
})
def create_or_update_product_api():
    data = request.form.to_dict()
    product_id = data.get('id')
    r.hset('product', product_id, json.dumps(data))
    return jsonify({'message': 'Product created/updated successfully'})

@app.route('/api/product/delete/<product_id>', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'product_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'The product ID'
        }
    ],
    'responses': {
        200: {
            'description': 'Product deleted successfully'
        }
    }
})
def delete_product_api(product_id):
    r.hdel('product', product_id)
    return jsonify({'message': 'Product deleted successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

