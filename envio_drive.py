import datetime
import time
import io
import json
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google_service import acessando_drive


def salvar_drive(funcao, caminho, nome, pasta_id=None):
    data_hora = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    drive = acessando_drive()
    time.sleep(1)
    file_metadata = {
        'name': f'{nome} - {data_hora}',
    }

    if pasta_id:
        file_metadata['parents'] = [pasta_id]
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
    file = drive.files().get(fileId=id, fields='id, name, mimeType').execute()
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
