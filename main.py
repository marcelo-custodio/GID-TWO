from flask import Flask, render_template, request, jsonify
from flask_restful import Api, Resource
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def chaves_rsa(num_bits):
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=num_bits)
    pem_private = private_key.private_bytes(encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption())

    public_key = private_key.public_key()
    pem_public = public_key.public_bytes(encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.PKCS1)
    
    return pem_private, pem_public

class Keys(Resource):
    def get(self):
        return jsonify({"healthcheck": "health"})

    def post(self):
        num_bits = request.form['num_bits']
        private_key, public_key = chaves_rsa(num_bits)
        return jsonify({'private': str(private_key), 'public': str(public_key)})

app = Flask(__name__)
api = Api(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

api.add_resource(Keys, '/api/keys')

if __name__ == '__main__':
    app.run(debug=True)