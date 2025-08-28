import requests
import os
from auxiliar import gerar_arquivo, gerar_data
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from autenticar import retornar_token
from envio_drive import buscar_json

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({"mensagem": "API para assistir na DCTFWeb - Rafael Costrov"})


@app.route('/darf', methods=['POST'])
def gerar_guia_dctfweb():
    load_dotenv()
    # Pegando parametros
    senha = request.form.get('senha')
    SENHA_API = os.getenv('SENHA_API')
    if senha != SENHA_API:
        return jsonify({"error": "Senha inválida"}), 403
    empresa = request.form.get('empresa')
    cnpj = request.form.get('cnpj')
    competencia = request.form.get('competencia')
    codigo = request.form.get('codigo')
    if not empresa or not cnpj or not competencia:
        return jsonify({"error": "Parâmetros inválidos"}), 400
    mensagem = "Guia DCTFWeb gerada com sucesso."

    # Gerando dados para a requisição
    ano, mes = competencia.split('-')
    dados = f'{{"categoria": "GERAL_MENSAL", "anoPA": "{ano}", "mesPA": "{mes}"}}'
    data = gerar_data(cnpj, "DCTFWEB", "GERARGUIA31", dados)
    nome_arquivo = f'DARF - {codigo} - {empresa} - {mes}-{ano}.pdf'
    url = 'https://gateway.apiserpro.serpro.gov.br/integra-contador/v1/Emitir'

    # Pegando pasta do drive para DARF
    PASTA_DRIVE_DCTFWEB_DARF = os.getenv('PASTA_DRIVE_DCTFWEB_DARF')

    # Chamando função auxiliar
    resultado_final = gerar_arquivo(
        empresa, cnpj, competencia, PASTA_DRIVE_DCTFWEB_DARF, url, data, nome_arquivo, mensagem
    )
    return resultado_final


@app.route('/darf-andamento', methods=['POST'])
def gerar_guia_dctfweb_andamento():
    load_dotenv()
    # Pegando parametros
    senha = request.form.get('senha')
    SENHA_API = os.getenv('SENHA_API')
    if senha != SENHA_API:
        return jsonify({"error": "Senha inválida"}), 403
    empresa = request.form.get('empresa')
    cnpj = request.form.get('cnpj')
    competencia = request.form.get('competencia')
    codigo = request.form.get('codigo')
    if not empresa or not cnpj or not competencia:
        return jsonify({"error": "Parâmetros inválidos"}), 400
    mensagem = "Guia DCTFWeb em andamento gerada com sucesso."

    # Gerando dados para a requisição
    ano, mes = competencia.split('-')
    dados = f'{{"categoria": "GERAL_MENSAL", "anoPA": "{ano}", "mesPA": "{mes}"}}'
    data = gerar_data(cnpj, "DCTFWEB", "GERARGUIAANDAMENTO313", dados)
    nome_arquivo = f'DARF andamento - {codigo} - {empresa} - {mes}-{ano}.pdf'
    url = 'https://gateway.apiserpro.serpro.gov.br/integra-contador/v1/Emitir'

    # Pegando pasta do drive para DARF em andamento
    PASTA_DRIVE_DCTFWEB_DARF_ANDAMENTO = os.getenv(
        'PASTA_DRIVE_DCTFWEB_DARF_ANDAMENTO')

    # Chamando função auxiliar
    resultado_final = gerar_arquivo(
        empresa, cnpj, competencia, PASTA_DRIVE_DCTFWEB_DARF_ANDAMENTO, url, data, nome_arquivo, mensagem
    )
    return resultado_final


@app.route('/recibo', methods=['POST'])
def gerar_recibo_dctfweb():
    # Pegando parametros
    senha = request.form.get('senha')
    SENHA_API = os.getenv('SENHA_API')
    if senha != SENHA_API:
        return jsonify({"error": "Senha inválida"}), 403
    empresa = request.form.get('empresa')
    cnpj = request.form.get('cnpj')
    competencia = request.form.get('competencia')
    codigo = request.form.get('codigo')
    if not empresa or not cnpj or not competencia:
        return jsonify({"error": "Parâmetros inválidos"}), 400
    mensagem = "Recibo DCTFWeb gerado com sucesso."

    # Gerando dados para a requisição
    ano, mes = competencia.split('-')
    dados = f'{{"categoria": "GERAL_MENSAL", "anoPA": "{ano}", "mesPA": "{mes}"}}'
    data = gerar_data(cnpj, "DCTFWEB", "CONSRECIBO32", dados)
    nome_arquivo = f'Recibo - {codigo} - {empresa} - {mes}-{ano}.pdf'
    url = 'https://gateway.apiserpro.serpro.gov.br/integra-contador/v1/Consultar'

    # Pegando pasta do drive para DARF
    PASTA_DRIVE_DCTFWEB_RECIBO = os.getenv('PASTA_DRIVE_DCTFWEB_RECIBO')

    # Chamando função auxiliar
    resultado_final = gerar_arquivo(
        empresa, cnpj, competencia, PASTA_DRIVE_DCTFWEB_RECIBO, url, data, nome_arquivo, mensagem
    )
    return resultado_final


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

        data = gerar_data(cnpj, "MIT", "ENCAPURACAO314", dados)

        requisicao = requests.post(
            url,
            headers=headers,
            json=data,
        )

        resposta = requisicao.json()
        print(resposta)
        verificador = verificar_json(resposta)
        if verificador:
            return verificador

        status = resposta.get('status')
        if status == 200:
            resultado = {
                "mensagem": "MIT gerado com sucesso.",
                "arquivo": id
            }
            return jsonify(resultado), 200
        else:
            return jsonify({"error": f"Erro ao gerar MIT - {resposta}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()
