from flask import Flask, render_template, request, jsonify
from flask_restful import Api, Resource
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Função responsável por gerar e salvar as chaves assimétricas RSA
def chaves_rsa(num_bits):
    # Geração da chave privada
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=num_bits)
    pem_private = private_key.private_bytes(encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption())
    # Salva a chave privada
    with open('keys/private_key.pem', 'wb') as f:
        f.write(pem_private)
        f.close()

    # Geração da chave pública
    public_key = private_key.public_key()
    pem_public = public_key.public_bytes(encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.PKCS1)
    # Salva a chave pública
    with open('keys/public_key.pem', 'wb') as f:
        f.write(pem_public)
        f.close()
    
    # retorno das chaves como string
    return pem_private.decode('UTF-8'), pem_public.decode('UTF-8')

# definição do endpoint /api/keys responsável por responder com chaves assimétricas RSA
class Keys(Resource):
    # Teste de disponibilidade do endpoint
    def get(self):
        return jsonify({"healthcheck": "health"})

    # Parse das entradas da interface e geração da resposta da API
    def post(self):
        num_bits = int(request.form['num_bits'])
        private_key, public_key = chaves_rsa(num_bits)
        return jsonify({'private': private_key, 'public': public_key})

# instanciação da API
app = Flask(__name__)
api = Api(app)

# definição/disponibilização do endpoint / responsável pela interface gráfica
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# disponibilização do endpoint /api/keys
api.add_resource(Keys, '/api/keys')

# disponibilização da API
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)