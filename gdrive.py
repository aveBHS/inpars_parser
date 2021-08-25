from config import config
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class GDrive:
    __slots__ = ('gauth', 'drive')

    def __init__(self):
        self.gauth = GoogleAuth()
        self.gauth.LoadCredentialsFile("google_credentials.txt")
        if self.gauth.credentials is None:
            self.gauth.LocalWebserverAuth()
        elif self.gauth.access_token_expired:
            self.gauth.Refresh()
        else:
            self.gauth.Authorize()
        self.gauth.SaveCredentialsFile("google_credentials.txt")

        self.drive = GoogleDrive(self.gauth)

    def upload_image(self, upload_file_list):
        for upload_file in upload_file_list:
            file = self.drive.CreateFile({'parents': [{'title': upload_file['name'], 'id': config("gdrive.folder")}]})
            file.SetContentFile(upload_file['file'])
            file.Upload()
            return 'https://drive.google.com/uc?export=view&id=' + file['id']


if __name__ == "__main__":
    gdrive = GDrive()
