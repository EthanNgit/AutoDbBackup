import os
from datetime import datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials

def export_database(username, password, database_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    backup_dir = os.path.join(script_dir, '..', 'backups')
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_file = f"{database_name}_backup_{timestamp}.sql"

    command = f"mysqldump -u {username} -p{password} {database_name} > {os.path.join(backup_dir, backup_file)}"
    os.system(command)

    backup_path = os.path.join(backup_dir, backup_file)
    print(f"Backup saved to: {backup_path}")
    return backup_path


def upload_to_drive(file_path):
    gauth = GoogleAuth()
    credentials_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials.json')
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file,
                                                                   scopes=['https://www.googleapis.com/auth/drive'])
    gauth.credentials = credentials
    drive = GoogleDrive(gauth)

    # Define the folder ID in your Google Drive where you want to save the backups
    folder_id = '000000000000'

    file_name = os.path.basename(file_path)
    file = drive.CreateFile({'title': file_name, 'parents': [{'id': folder_id}]})
    file.SetContentFile(file_path)
    try:
        file.Upload()
    except Exception as e:
        print(f"Error uploading file to Google Drive: {e}")
        return

    # Share the uploaded file with your personal account
    try:
        permission = file.InsertPermission({
            'type': 'user',
            'value': 'username@gmail.com', # Put personal gmail to share files with
            'role': 'reader'  # Change the role as needed (e.g., 'reader', 'writer', 'owner')
        })
    except Exception as e:
        print(f"Error sharing file with personal account: {e}")

    # Delete older (than 7 days) backup files on Google Drive
    for old_file in drive.ListFile({'q': f"'{folder_id}' in parents and title contains '{file_name.split('_')[0]}' and trashed=false"}).GetList():
        created_time = datetime.strptime(old_file['createdDate'], "%Y-%m-%dT%H:%M:%S.%fZ")
        if (datetime.now() - created_time).days > 7:
            try:
                old_file.Delete()
            except Exception as e:
                print(f"Error deleting old backup file on Google Drive: {e}")
    try:
        os.remove(file_path)
    except Exception as e:
        print(f"Error deleting local backup file: {e}")

def main():
    # For every database you want to backup, put the name here
    databases = ['database1', 'database2']
    for database in databases:
        backup_file = export_database('username', 'password', database)
        upload_to_drive(backup_file)

if __name__ == "__main__":
    main()
