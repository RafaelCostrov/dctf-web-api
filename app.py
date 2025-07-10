import requests
import os
import json
import base64
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from autenticar import retornar_token
from envio_drive import salvar_drive

app = Flask(__name__)


@app.route('/')
def index():
    return "API para assistir na DCTFWeb - Rafael Costrov"


@app.route('/darf', methods=['POST'])
def gerar_guia_dctfweb():
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
    empresa = request.form.get('empresa')
    cnpj = request.form.get('cnpj')
    competencia = request.form.get('competencia')
    if not empresa or not cnpj or not competencia:
        return jsonify({"error": "Parâmetros inválidos"}), 400
    try:
        load_dotenv()
        PASTA_DRIVE_DCTFWEB_DARF = os.getenv('PASTA_DRIVE_DCTFWEB_RECIBO')
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
            '', nome_arquivo, nome_arquivo, PASTA_DRIVE_DCTFWEB_DARF)
        resultado = {
            "mensagem": "Recibo DCTFWeb gerado com sucesso.",
            "fileId": arquivo_drive
        }
        if os.path.exists(nome_arquivo):
            os.remove(nome_arquivo)
        return resultado, 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# def gerar_mit():

#     cnpj = input("Digite o CNPJ (somente números): ")

#     access_token, jwt = retornar_token()

#     url = 'https://gateway.apiserpro.serpro.gov.br/integra-contador/v1/Declarar'

#     headers = {
#         'Authorization': f'Bearer {access_token}',
#         'Content-Type': 'application/json',
#         'jwt_token': jwt,
#     }

#     with open("15435766-MIT-202506.JSON", "r", encoding="utf-8") as f:
#         dados = f.read()
#     print(dados)
#     data = {
#         "contratante": {
#             "numero": "15435766000176",
#             "tipo": 2
#         },
#         "autorPedidoDados": {
#             "numero": "15435766000176",
#             "tipo": 2
#         },
#         "contribuinte": {
#             "numero": f"{cnpj}",
#             "tipo": 2
#         },
#         "pedidoDados": {
#             "idSistema": "MIT",
#             "idServico": "ENCAPURACAO314",
#             "versaoSistema": "1.0",
#             "dados": dados
#         }
#     }

#     requisicao = requests.post(
#         url,
#         headers=headers,
#         json=data,
#     )
#     print(request.text)
#     print(request.status_code)


# if __name__ == "__main__":
#     print("Escolha uma opção:")
#     print("1. Gerar Guia DCTFWeb")
#     print("2. Gerar Recibo DCTFWeb")
#     print("3. Gerar MIT")

#     opcao = input("Digite o número da opção: ")

#     if opcao == '1':
#         gerar_guia_dctfweb()
#     elif opcao == '2':
#         gerar_recibo_dctfweb()
#     elif opcao == '3':
#         gerar_mit()
#     else:
#         print("Opção inválida.")


if __name__ == "__main__":
    app.run()
