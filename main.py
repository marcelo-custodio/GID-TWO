from flask import Flask, render_template, request, jsonify
from flask_restful import Api, Resource
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def chaves_rsa(num_bits):
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=num_bits)
    pem_private = private_key.private_bytes(encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption())
    with open('keys/private_key.pem', 'wb') as f:
        f.write(pem_private)
        f.close()

    public_key = private_key.public_key()
    pem_public = public_key.public_bytes(encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.PKCS1)
    with open('keys/public_key.pem', 'wb') as f:
        f.write(pem_public)
        f.close()
    
    return pem_private.decode('UTF-8'), pem_public.decode('UTF-8')

class Keys(Resource):
    def get(self):
        return jsonify({"healthcheck": "health"})

    def post(self):
        num_bits = int(request.form['num_bits'])
        private_key, public_key = chaves_rsa(num_bits)
        return jsonify({'private': private_key, 'public': public_key})

app = Flask(__name__)
api = Api(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

api.add_resource(Keys, '/api/keys')

if __name__ == '__main__':
    app.run(debug=True)