import datetime
import time
import io
import json
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google_service import acessando_drive


def salvar_drive(mes, ano, caminho, nome, pasta_id=None):
    data_hora = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    drive = acessando_drive()
    time.sleep(1)
    competencia = f"{mes}/{ano}"

    subpasta = None
    if pasta_id:
        query = f"'{pasta_id}' in parents and mimeType = 'application/vnd.google-apps.folder' and name = '{competencia}' and trashed = false"
        results = drive.files().list(q=query, fields="files(id, name)").execute()
        pastas = results.get('files', [])

        if pastas:
            subpasta = pastas[0]['id']
        else:
            file_metadata = {
                'name': competencia,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [pasta_id]
            }
            pasta_criada = drive.files().create(body=file_metadata, fields='id').execute()
            subpasta = pasta_criada['id']

    nome_formatado = nome.replace('.pdf', '')
    file_metadata = {
        'name': f'{nome_formatado} - {data_hora}',
        'parents': [subpasta]
    }

    media = MediaFileUpload(caminho, mimetype='application/pdf')

    file = drive.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    return file


def buscar_json(id):
    drive = acessando_drive()
    time.sleep(1)
    file = drive.files().get(fileId=id, fields='id,name,mimeType').execute()
    if not file['mimeType'] == 'application/json':
        raise ValueError("O arquivo não é do tipo JSON.")
    request = drive.files().get_media(fileId=id)
    arquivo = io.BytesIO()
    downloader = MediaIoBaseDownload(arquivo, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()

    arquivo.seek(0)
    dados = arquivo.read().decode('utf-8')
    return dados
