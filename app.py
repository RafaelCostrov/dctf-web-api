import requests
import os
import json
import base64
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from autenticar import retornar_token
from envio_drive import salvar_drive, buscar_json

app = Flask(__name__)


def gerar_data(cnpj, id_sistema, id_servico, dados):
    json_data = {
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
            "idSistema": id_sistema,
            "idServico": id_servico,
            "versaoSistema": "1.0",
            "dados": dados
        }
    }
    return json_data


def verificar_json(json):
    codigo_sem_procuracao = "[AcessoNegado-ICGERENCIADOR-022]"
    sem_procuracao = any(mensagem.get("codigo") ==
                         codigo_sem_procuracao for mensagem in json.get("mensagens", []))
    if sem_procuracao:
        return jsonify({"error": "Sem procuração para a Oraculu's."}), 403

    codigo_declaracao_inexistente = "[Aviso-DCTFWEB-MG08]"
    nao_encontrada = any(mensagem.get("codigo") ==
                         codigo_declaracao_inexistente for mensagem in json.get("mensagens", []))
    if nao_encontrada:
        return jsonify({"error": "Declaração não encontrada."}), 404

    codigo_em_andamento = "[EntradaIncorreta-DCTFWEB-MG10]"
    em_andamento = any(mensagem.get("codigo") ==
                       codigo_em_andamento for mensagem in json.get("mensagens", []))
    if em_andamento:
        return jsonify({"error": "Declaração em andamento."}), 404

    codigo_mit_em_andamento = "[Aviso-MIT-MSG_0036]"
    mit_em_andamento = any(mensagem.get("codigo") ==
                           codigo_mit_em_andamento for mensagem in json.get("mensagens", []))
    if mit_em_andamento:
        return jsonify({"error": "Existe uma apuração MIT em andamento."}), 404

    return None


@app.route('/')
def index():
    return jsonify({"mensagem": "API para assistir na DCTFWeb - Rafael Costrov"})


@app.route('/darf', methods=['POST'])
def gerar_guia_dctfweb():
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
        data = gerar_data(cnpj, "DCTFWEB", "GERARGUIA31", dados)

        requisicao = requests.post(
            url,
            headers=headers,
            json=data,
        )

        resposta = requisicao.json()
        verificador = verificar_json(resposta)
        if verificador:
            return verificador
        dados_json = resposta.get('dados', {})
        pdfBase64 = json.loads(dados_json).get('PDFByteArrayBase64')
        pdf_bytes = base64.b64decode(pdfBase64)
        nome_arquivo = f'DARF - {codigo} - {empresa} - {mes}-{ano}.pdf'
        with open(nome_arquivo, 'wb') as pdf_file:
            pdf_file.write(pdf_bytes)
        arquivo_drive = salvar_drive(
            mes, ano, nome_arquivo, nome_arquivo, PASTA_DRIVE_DCTFWEB_DARF)
        resultado = {
            "mensagem": "Guia DCTFWeb gerada com sucesso.",
            "fileId": arquivo_drive
        }
        if os.path.exists(nome_arquivo):
            os.remove(nome_arquivo)
        status = resposta.get('status')
        if status == 200:
            return jsonify(resultado), 200
        else:
            return jsonify({"error": f"Erro ao gerar guia DCTFWeb - {resposta}"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/recibo', methods=['POST'])
def gerar_recibo_dctfweb():
    senha = request.form.get('senha')
    SENHA_API = os.getenv('SENHA_API')
    if senha != SENHA_API:
        return jsonify({"error": "Senha inválida"}), 403
    empresa = request.form.get('empresa')
    codigo = request.form.get('codigo')
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
        data = gerar_data(cnpj, "DCTFWEB", "CONSRECIBO32", dados)

        requisicao = requests.post(
            url,
            headers=headers,
            json=data,
        )

        resposta = requisicao.json()
        verificador = verificar_json(resposta)
        if verificador:
            return verificador
        dados_json = resposta.get('dados', {})
        pdfBase64 = json.loads(dados_json).get('PDFByteArrayBase64')
        pdf_bytes = base64.b64decode(pdfBase64)
        nome_arquivo = f'Recibo - {codigo} - {empresa} - {mes}-{ano}.pdf'
        with open(nome_arquivo, 'wb') as pdf_file:
            pdf_file.write(pdf_bytes)
        arquivo_drive = salvar_drive(
            mes, ano, nome_arquivo, nome_arquivo, PASTA_DRIVE_DCTFWEB_RECIBO)
        resultado = {
            "mensagem": "Recibo DCTFWeb gerado com sucesso.",
            "fileId": arquivo_drive
        }
        if os.path.exists(nome_arquivo):
            os.remove(nome_arquivo)
        status = resposta.get('status')
        if status == 200:
            return jsonify(resultado), 200
        else:
            return jsonify({"error": f"Erro ao gerar o recibo DCTFWeb - {resposta}"}), 500

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
