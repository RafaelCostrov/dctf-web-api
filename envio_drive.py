import datetime
import time
from googleapiclient.http import MediaFileUpload
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
