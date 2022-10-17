from data import *
from googleapiclient.http import MediaFileUpload
import pandas as pd
from discord import Attachment


folder_ids = {'Resources':'1eZUlMDX_jrwU-6-CuucqZfuMPH251R7k'}
file_ids = {}


def get_folder_ids():
    """
    Collects the folder ids
    """
    results = drive_service.files().list(
        fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    items.pop(0)
    if not items:
        print('No files found.')
    else:
        for item in items:
            folder_ids[item['name']] = item['id']


def get_all_folders() -> list:
    """
    Retrieves all folder names from the drive and sends them as an Array[str]
    """
    query = f"parents = '{folder_ids['Resources']}'"
    response = drive_service.files().list(q=query).execute()
    files = response.get('files')
    nextPageToken = response.get('nextPageToken')

    while nextPageToken:
        response = drive_service.files().list(q=query).execute()
        files.extend(response.get('files'))
        nextPageToken = response.get('nextPageToken')
    df = pd.DataFrame(files)
    df_files = df[df['mimeType'] == 'application/vnd.google-apps.folder']

    folders = df_files['name'].tolist()
    return folders


def create_drive_folder(folder: str) -> bool:
    """
    Creates folder in said google drive using provided folder name and returns whether successful or not
    """
    file_metadata = {'name': folder, 'mimeType':'application/vnd.google-apps.folder','parents':[folder_ids['Resources']]}
    drive_service.files().create(body=file_metadata).execute()
    return True


def get_all_files(folder: str) -> list:
    """
    Retrieves all file names from the specified folder in drive and sends them as an Array[str]
    """
    get_folder_ids()
    query = f"parents = '{folder_ids[folder]}'"
    response = drive_service.files().list(q=query).execute()
    files = response.get('files')
    nextPageToken = response.get('nextPageToken')

    while nextPageToken:
        response = drive_service.files().list(q=query).execute()
        files.extend(response.get('files'))
        nextPageToken = response.get('nextPageToken')
    df = pd.DataFrame(files)
    df_files = df[df['mimeType'] != 'application/vnd.google-apps.folder']
    for index, row in df_files.iterrows():
        name = row['name']
        id = row['id']
        file_ids[name] = id

    files = df_files['name'].tolist()
    return files


def get_file(folder: str, file: str) -> str:
    """
    Retrieves google drive file from specified folder and file name
    :return file link
    """
    get_all_files(folder)
    link = drive_service.files().get(fileId=file_ids[file], fields='webViewLink').execute()
    return link['webViewLink']


def upload_file(filename: str, filepath: str, drivepath: str) -> bool:
    """
    Uploads a file to the specified folder with the given filename taken from the filepath
    returns whether it was successful or not
    """
    get_folder_ids()
    file_metadata = {'name': filename, 'parents': [folder_ids[drivepath]]}
    media = MediaFileUpload(filepath, mimetype='application/pdf')
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return True


async def download_file(file: Attachment) -> str:
    """
    return file save path
    """
    path = r"D:\Resources\Machine Learning\pythonProject\{0}".format(
        file.filename)
    await file.save(path)
    return path
