import requests
import os
import json
import base64
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from autenticar import retornar_token
from envio_drive import salvar_drive, buscar_json

app = Flask(__name__)


@app.route('/')
def index():
    return "API para assistir na DCTFWeb - Rafael Costrov"


@app.route('/darf', methods=['POST'])
def gerar_guia_dctfweb():
    senha = request.form.get('senha')
    SENHA_API = os.getenv('SENHA_API')
    if senha != SENHA_API:
        return jsonify({"error": "Senha inválida"}), 403
    empresa = request.form.get('empresa')
    cnpj = request.form.get('cnpj')
    competencia = request.form.get('competencia')
    if not empresa or not cnpj or not competencia:
        return jsonify({"error": "Parâmetros inválidos"}), 400
    try:

        load_dotenv()
        PASTA_DRIVE_DCTFWEB_DARF = os.getenv('PASTA_DRIVE_DCTFWEB_DARF')
        ano, mes = competencia.split('-')
        access_token, jwt = retornar_token()
        url = 'https://gateway.apiserpro.serpro.gov.br/integra-contador/v1/Emitir'

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'jwt_token': jwt,
        }

        dados = f'{{"categoria": "GERAL_MENSAL", "anoPA": "{ano}", "mesPA": "{mes}"}}'

        data = {
            "contratante": {
                "numero": "15435766000176",
                "tipo": 2
            },
            "autorPedidoDados": {
                "numero": "15435766000176",
                "tipo": 2
            },
            "contribuinte": {
                "numero": f"{cnpj}",
                "tipo": 2
            },
            "pedidoDados": {
                "idSistema": "DCTFWEB",
                "idServico": "GERARGUIA31",
                "versaoSistema": "1.0",
                "dados": dados
            }
        }

        requisicao = requests.post(
            url,
            headers=headers,
            json=data,
        )

        dados_json = requisicao.json().get('dados', {})
        pdfBase64 = json.loads(dados_json).get('PDFByteArrayBase64')
        pdf_bytes = base64.b64decode(pdfBase64)
        nome_arquivo = f'DARF - {empresa} - {mes}-{ano}.pdf'
        with open(nome_arquivo, 'wb') as pdf_file:
            pdf_file.write(pdf_bytes)
        arquivo_drive = salvar_drive(
            '', nome_arquivo, nome_arquivo, PASTA_DRIVE_DCTFWEB_DARF)
        resultado = {
            "mensagem": "Guia DCTFWeb gerada com sucesso.",
            "fileId": arquivo_drive
        }
        if os.path.exists(nome_arquivo):
            os.remove(nome_arquivo)
        return resultado, 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/recibo', methods=['POST'])
def gerar_recibo_dctfweb():
    print(request.form)
    senha = request.form.get('senha')
    SENHA_API = os.getenv('SENHA_API')
    if senha != SENHA_API:
        return jsonify({"error": "Senha inválida"}), 403
    empresa = request.form.get('empresa')
    cnpj = request.form.get('cnpj')
    competencia = request.form.get('competencia')
    if not empresa or not cnpj or not competencia:
        return jsonify({"error": "Parâmetros inválidos"}), 400
    try:
        load_dotenv()
        PASTA_DRIVE_DCTFWEB_RECIBO = os.getenv('PASTA_DRIVE_DCTFWEB_RECIBO')
        ano, mes = competencia.split('-')
        access_token, jwt = retornar_token()
        url = 'https://gateway.apiserpro.serpro.gov.br/integra-contador/v1/Consultar'

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'jwt_token': jwt,
        }

        dados = f'{{"categoria": "GERAL_MENSAL", "anoPA": "{ano}", "mesPA": "{mes}"}}'

        data = {
            "contratante": {
                "numero": "15435766000176",
                "tipo": 2
            },
            "autorPedidoDados": {
                "numero": "15435766000176",
                "tipo": 2
            },
            "contribuinte": {
                "numero": f"{cnpj}",
                "tipo": 2
            },
            "pedidoDados": {
                "idSistema": "DCTFWEB",
                "idServico": "CONSRECIBO32",
                "versaoSistema": "1.0",
                "dados": dados
            }
        }

        requisicao = requests.post(
            url,
            headers=headers,
            json=data,
        )

        dados_json = requisicao.json().get('dados', {})
        pdfBase64 = json.loads(dados_json).get('PDFByteArrayBase64')
        pdf_bytes = base64.b64decode(pdfBase64)
        nome_arquivo = f'Recibo - {empresa} - {mes}-{ano}.pdf'
        with open(nome_arquivo, 'wb') as pdf_file:
            pdf_file.write(pdf_bytes)
        arquivo_drive = salvar_drive(
            '', nome_arquivo, nome_arquivo, PASTA_DRIVE_DCTFWEB_RECIBO)
        resultado = {
            "mensagem": "Recibo DCTFWeb gerado com sucesso.",
            "fileId": arquivo_drive
        }
        if os.path.exists(nome_arquivo):
            os.remove(nome_arquivo)
        return resultado, 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/mit', methods=['POST'])
def gerar_mit():
    load_dotenv()
    senha = request.form.get('senha')
    SENHA_API = os.getenv('SENHA_API')
    if senha != SENHA_API:
        return jsonify({"error": "Senha inválida"}), 403
    try:
        access_token, jwt = retornar_token()
        empresa = request.form.get('empresa')
        cnpj = request.form.get('cnpj')
        id = request.form.get('fileId')
        dados = buscar_json(id)
        if not empresa or not cnpj or not dados:
            return jsonify({"error": "Parâmetros inválidos"}), 400
        url = 'https://gateway.apiserpro.serpro.gov.br/integra-contador/v1/Declarar'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'jwt_token': jwt,
        }

        data = {
            "contratante": {
                "numero": "15435766000176",
                "tipo": 2
            },
            "autorPedidoDados": {
                "numero": "15435766000176",
                "tipo": 2
            },
            "contribuinte": {
                "numero": f"{cnpj}",
                "tipo": 2
            },
            "pedidoDados": {
                "idSistema": "MIT",
                "idServico": "ENCAPURACAO314",
                "versaoSistema": "1.0",
                "dados": dados
            }
        }

        requisicao = requests.post(
            url,
            headers=headers,
            json=data,
        )

        resposta = requisicao.json()
        status = resposta.get('status')
        if status == 200:
            resultado = {
                "mensagem": "MIT gerado com sucesso.",
                "arquivo": id
            }
            print(resposta)
            return jsonify(resultado), 200
        else:
            print(f"Erro ao gerar MIT: {resposta}")
            return jsonify({"error": "Erro ao gerar MIT"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()
