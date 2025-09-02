from flask import jsonify, request
from autenticar import retornar_token
from envio_drive import salvar_drive
import json
import os
import requests
import base64


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


def gerar_salvar_arquivo(nome_arquivo, pdf_bytes, mes, ano, pasta, mensagem):
    with open(nome_arquivo, 'wb') as pdf_file:
        pdf_file.write(pdf_bytes)
    arquivo_drive = salvar_drive(
        mes, ano, nome_arquivo, nome_arquivo, pasta)
    return {
        "mensagem": mensagem,
        "fileId": arquivo_drive
    }


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

    texto_sem_em_andamento = "Utilize o serviço GERARGUIA31"
    sem_em_andamento = any(texto_sem_em_andamento in mensagem.get(
        "texto") for mensagem in json.get("mensagens", []))

    if sem_em_andamento:
        return jsonify({"error": "Sem declaração em andamento. Utilize a opção 'DARF'."}), 404

    texto_sem_debito = "Não há débitos com saldo a pagar para emissão da guia de pagamento."
    sem_debito = any(texto_sem_debito in mensagem.get(
        "texto") for mensagem in json.get("mensagens", []))

    if sem_debito:
        return jsonify({"error": "Não há débitos para a opção selecionada."}), 404

    codigo_em_andamento = "[EntradaIncorreta-DCTFWEB-MG10]"
    em_andamento = any(mensagem.get("codigo") ==
                       codigo_em_andamento for mensagem in json.get("mensagens", []))
    if em_andamento:
        return jsonify({"error": "Declaração em andamento."}), 404

    codigo_mit_em_andamento = "[Aviso-MIT-MSG_0036]"
    mit_em_andamento = any(mensagem.get("codigo") ==
                           codigo_mit_em_andamento for mensagem in json.get("mensagens", []))
    if mit_em_andamento:
        return jsonify({"error": "Existe uma apuração MIT em andamento."}), 400

    return None


def gerar_arquivo(empresa, cnpj, competencia, pasta, url, data, nome_arquivo, mensagem):
    if not empresa or not cnpj or not competencia:
        return jsonify({"error": "Dados incompletos"}), 400

    try:
        ano, mes = competencia.split('-')
        access_token, jwt = retornar_token()

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'jwt_token': jwt,
        }

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

        dados_json = resposta.get('dados', {})
        pdfBase64 = json.loads(dados_json).get('PDFByteArrayBase64')
        pdf_bytes = base64.b64decode(pdfBase64)

        resultado = gerar_salvar_arquivo(
            nome_arquivo, pdf_bytes, mes, ano, pasta, mensagem
        )

        if os.path.exists(nome_arquivo):
            os.remove(nome_arquivo)

        status = resposta.get('status')
        if status == 200:
            return jsonify(resultado), 200
        else:
            return jsonify({"error": f"Erro ao gerar arquivo - {resposta}"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500
