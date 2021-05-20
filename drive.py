import os
import pickle
import json
from requests.utils import quote
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config import DRIVE_NAME, DRIVE_ID, INDEX_URL


SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']


class GoogleDriveHelper:
    def __init__(self, name=None, listener=None):
        self.__G_DRIVE_TOKEN_FILE = "token.pickle"
        self.__OAUTH_SCOPE = ['https://www.googleapis.com/auth/drive']
        self.__service = self.authorize()
        self.path = []

    def get_readable_file_size(self, size_in_bytes) -> str:
        if size_in_bytes is None:
            return '0B'
        index = 0
        size_in_bytes = int(size_in_bytes)
        while size_in_bytes >= 1024:
            size_in_bytes /= 1024
            index += 1
        try:
            return f'{round(size_in_bytes, 2)}{SIZE_UNITS[index]}'
        except IndexError:
            return 'File too large'

    def authorize(self):
        # Get credentials
        credentials = None
        if os.path.exists(self.__G_DRIVE_TOKEN_FILE):
            with open(self.__G_DRIVE_TOKEN_FILE, 'rb') as f:
                credentials = pickle.load(f)
        if credentials is None or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.__OAUTH_SCOPE)
                credentials = flow.run_console(port=0)

            # Save the credentials for the next run
            with open(self.__G_DRIVE_TOKEN_FILE, 'wb') as token:
                pickle.dump(credentials, token)
        return build('drive', 'v3', credentials=credentials, cache_discovery=False)

    def drive_query(self, parent_id, fileName):
        fileName = fileName.replace("'","\\'").replace('"','\\"')
        gquery = " and ".join([f"name contains '{x}'" for x in fileName.split()])
        query = f"'{parent_id}' in parents and ({gquery})"
        response = self.__service.files().list(supportsTeamDrives=True,
                                               includeTeamDriveItems=True,
                                               q=query,
                                               spaces='drive',
                                               pageSize=200,
                                               fields='files(id, name, mimeType, size)',
                                               orderBy='modifiedTime desc').execute()["files"]
        return response

    def drive_list(self, fileName):
        msg = ''
        data = []
        INDEX = -1
        for parent_id in DRIVE_ID:
            response = self.drive_query(parent_id, fileName)
            INDEX += 1
            for file in response:
                if file['mimeType'] == "application/vnd.google-apps.folder":
                    url_path = quote(f"{file['name']}")
                    url = f'{INDEX_URL[INDEX]}/{url_path}/'
                    data.append(
                            {
                                "type": "folder",
                                "name": file['name'],
                                "size": "none",
                                "url": url,
                                "drive_url": f"https://drive.google.com/drive/folders/{file['id']}"
                                }
                            )
                else:
                    size = self.get_readable_file_size(file.get('size'))
                    url_path = quote(f'{file.get("name")}')
                    url = f'{INDEX_URL[INDEX]}/{url_path}'
                    data.append(
                        {
                            "type": "file",
                            "name": file['name'],
                            "size": size,
                            "url": url,
                            "drive_url": f"https://drive.google.com/uc?id={file['id']}&export=download"
                            }
                        )
        # if len(data) == 0:
        #     return {"error": "Found Literally Nothing"}
        return data

drive = GoogleDriveHelper(None)
