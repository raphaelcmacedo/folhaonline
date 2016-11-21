import os
import tempfile

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def insert_file(contra_cheque, file, mime_type = 'application/pdf'):

    drive = _auth()

    #Arquivo temporário
    fd, tmp = tempfile.mkstemp()
    with os.fdopen(fd, 'wb+') as out:
        for chunk in file.chunks():
            out.write(chunk)

    #Realiza o upload
    upload = drive.CreateFile()
    file_name = '{}-{}-{}/{}.pdf'.format(contra_cheque.matricula.orgao.sigla, contra_cheque.matricula.numero, contra_cheque.mes, contra_cheque.exercicio)
    upload['title'] = file_name
    upload.SetContentFile(tmp)
    upload.Upload()

    #Busca a url
    url = upload['downloadUrl']
    index = url.index('?')
    if(index > 0):
        url = url[:index]

    contra_cheque.url = url

def _auth():
    gauth = GoogleAuth()

    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("mycreds.txt")

    return GoogleDrive(gauth)