from flask import Flask, jsonify, request
from flask_cors import CORS
from DAO import DAO
from Models import Alimento, Nutriente, AlimentoNutriente
from DB import get_session

app = Flask(__name__)
CORS(app)  # Libera o acesso ao front-end

dao = DAO()

# =================== Rotas =====================

@app.route("/")
def index():
    return "API do NutriApp funcionando! 🍎"

# Buscar alimentos por categoria (GET)
@app.route("/alimentos/categoria/<categoria>", methods=["GET"])
def get_alimentos_por_categoria(categoria):
    try:
        resultados = dao.buscar_por_categoria(categoria)
        alimentos = [
            {
                "id_alimento": row[0],
                "nome_alimento": row[1],
                "unidade_padrao": row[2],
                "calorias": row[3],
            }
            for row in resultados
        ]
        return jsonify(alimentos)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# Criar novo alimento (POST)
@app.route("/alimentos", methods=["POST"])
def adicionar_alimento():
    dados = request.get_json()
    novo_alimento = Alimento(
        nome_alimento=dados["nome_alimento"],
        unidade_padrao=dados["unidade_padrao"],
        calorias=dados["calorias"],
        id_categoria=dados["id_categoria"]
    )
    try:
        resultado = dao.adicionar_entidade(novo_alimento)
        return jsonify({
            "id_alimento": resultado.id_alimento,
            "mensagem": "Alimento adicionado com sucesso!"
        }), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# Obter alimento por ID (GET)
@app.route("/alimentos/<int:id_alimento>", methods=["GET"])
def get_alimento(id_alimento):
    try:
        alimento = dao.obter_por_id(Alimento, id_alimento)
        return jsonify({
            "id_alimento": alimento.id_alimento,
            "nome_alimento": alimento.nome_alimento,
            "unidade_padrao": alimento.unidade_padrao,
            "calorias": alimento.calorias,
            "id_categoria": alimento.id_categoria
        })
    except Exception as e:
        return jsonify({"erro": str(e)}), 404

# Remover alimento (DELETE)
@app.route("/alimentos/<int:id_alimento>", methods=["DELETE"])
def deletar_alimento(id_alimento):
    try:
        sucesso = dao.remover_por_id(Alimento, id_alimento)
        if sucesso:
            return jsonify({"mensagem": "Alimento deletado com sucesso!"})
        return jsonify({"mensagem": "Alimento não encontrado."}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    
# Obter todos os alimentos da tabela    
@app.route("/alimentos", methods=["GET"])
def get_todos_alimentos():
    try:
        with get_session() as session:
            alimentos = session.query(Alimento).all()
            lista = [
                {
                    "id_alimento": a.id_alimento,
                    "nome_alimento": a.nome_alimento,
                    "unidade_padrao": a.unidade_padrao,
                    "calorias": a.calorias,
                    "id_categoria": a.id_categoria
                }
                for a in alimentos
            ]
            return jsonify(lista)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    
# Obter alimento por nome (GET)
@app.route("/alimentos/nome/<nome_alimento>", methods=["GET"])
def get_alimento_por_nome(nome_alimento):
    try:
        with get_session() as session:
            alimento = session.query(Alimento).filter(Alimento.nome_alimento == nome_alimento).first()
            if alimento:
                return jsonify({
                    "id_alimento": alimento.id_alimento,
                    "nome_alimento": alimento.nome_alimento,
                    "unidade_padrao": alimento.unidade_padrao,
                    "calorias": alimento.calorias,
                    "id_categoria": alimento.id_categoria
                })
            else:
                return jsonify({"erro": "Alimento não encontrado."}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    
@app.route("/alimentos/nutrientes/<nome_alimento>", methods=["GET"])
def get_nutrientes_por_alimento(nome_alimento):
    try:
        with get_session() as session:
            # 1. Buscar alimento pelo nome
            alimento = session.query(Alimento).filter(Alimento.nome_alimento == nome_alimento).first()

            if not alimento:
                return jsonify({"erro": "Alimento não encontrado."}), 404

            # 2. Buscar os nutrientes relacionados ao alimento
            nutrientes = (
                session.query(AlimentoNutriente, Nutriente)
                .join(Nutriente, AlimentoNutriente.id_nutriente == Nutriente.id_nutriente)
                .filter(AlimentoNutriente.id_alimento == alimento.id_alimento)
                .all()
            )

            # 3. Montar resposta
            resultado = {
                "id_alimento": alimento.id_alimento,
                "nome_alimento": alimento.nome_alimento,
                "unidade_padrao": alimento.unidade_padrao,
                "calorias": alimento.calorias,
                "nutrientes": [
                    {
                        "id_nutriente": nutriente.id_nutriente,
                        "nome_nutriente": nutriente.nome_nutriente,
                        "unidade_medida": nutriente.unidade_medida,
                        "quantidade_por_100un": alimento_nutriente.quantidade_por_100un
                    }
                    for alimento_nutriente, nutriente in nutrientes
                ]
            }

            return jsonify(resultado)

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# ==============================================

if __name__ == "__main__":
    app.run(debug=True)
