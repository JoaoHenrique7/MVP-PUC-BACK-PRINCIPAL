from flask import Flask, request
from flask_cors import CORS
from flask_restx import Api, Resource, fields
import requests
import model

app = Flask(__name__)
CORS(app)

# API com Swagger
api = Api(app, version="1.0", title="API de Endereços",
          description="CRUD de endereços usando ViaCEP e SQLite")

# Namespace
ns = api.namespace("enderecos", description="Operações com endereços")

# Modelo para Swagger
endereco_model = api.model("Endereco", {
    "id": fields.Integer(readonly=True),
    "cep": fields.String(required=True, description="CEP do endereço"),
    "logradouro": fields.String(description="Logradouro"),
    "bairro": fields.String(description="Bairro"),
    "localidade": fields.String(description="Cidade"),
    "uf": fields.String(description="UF"),
})

# Inicializa DB
model.init_db()

# ---------- Rotas ----------

@ns.route("")
class EnderecoList(Resource):
    @ns.marshal_list_with(endereco_model)
    def get(self):
        """Lista todos os endereços"""
        return model.get_enderecos()

    @ns.expect(api.model("CEPInput", {"cep": fields.String(required=True)}))
    @ns.marshal_with(endereco_model, code=201)
    def post(self):
        """Adiciona um endereço consultando ViaCEP"""
        data = request.get_json()
        cep = data.get("cep")
        if not cep:
            api.abort(400, "CEP é obrigatório")

        resp = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
        if resp.status_code != 200:
            api.abort(500, "Erro ao consultar ViaCEP")

        dados = resp.json()
        if "erro" in dados:
            api.abort(404, "CEP inválido")

        model.insert_endereco(
            cep,
            dados.get("logradouro"),
            dados.get("bairro"),
            dados.get("localidade"),
            dados.get("uf"),
        )
        return dados, 201

@ns.route("/<int:endereco_id>")
@ns.param("endereco_id", "ID do endereço")
class Endereco(Resource):
    @ns.expect(endereco_model)
    def put(self, endereco_id):
        """Atualiza um endereço pelo ID"""
        data = request.get_json()
        updated = model.update_endereco(
            endereco_id,
            data.get("logradouro"),
            data.get("bairro"),
            data.get("localidade"),
            data.get("uf"),
        )
        if updated == 0:
            api.abort(404, "Endereço não encontrado")
        return {"message": "Endereço atualizado com sucesso"}

    def delete(self, endereco_id):
        """Deleta um endereço pelo ID"""
        deleted = model.delete_endereco(endereco_id)
        if deleted == 0:
            api.abort(404, "Endereço não encontrado")
        return {"message": "Endereço deletado com sucesso"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
