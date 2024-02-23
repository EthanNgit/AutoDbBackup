# Automatic database bakup generator
This was made for an ubuntu machine, the idea is it dumps a copy of the database (using mariadb) and pushes it to a google drive.

## To use

### Step 1
First import the files to your machine my file structure look something like this

usr/</br>
├─ local/</br>
│  ├─ bin/</br>
│  │  ├─ auto-db-backup/</br>
│  │  │  ├─ scripts/</br>
│  │  │  │  ├─ main.py/</br>
│  │  │  │  ├─ run.py/</br>
│  │  │  │  ├─ credentials.json/</br>
│  │  │  ├─ backups/</br>
│  │  │  ├─ venv/</br>

Where backups is generated by the script and venv is the virtual environment you should create to hold the pydrive import.

### Step 2 
Create a Service Account:

Go to the Google Cloud Console: https://console.cloud.google.com/. </br>
Create a new project or select an existing one.</br>
Navigate to the "IAM & Admin" > "Service Accounts" section.</br>
Click on "Create service account".</br>
Give your service account a name and click "Create".</br>

Generate JSON Key File:

After creating the service account, click on it from the list of service accounts.</br>
Go to the "Keys" tab and click on "Add Key" > "Create new key".</br>
Choose JSON as the key type and click "Create". This will download a JSON key file containing your credentials.</br>

Fill in data:

Place the new credentials.json where the filler one was.</br>
Replace the email with your email in main.py</br>
Fill in all databases you want to backup into the array.</br>
Make sure to pass in a authorized user account's username and password to access your database.</br>

Getting Folder id:

To get the folder id go to the google drive account you want to share the backups with and copy the link of the folder you want them to go into</br>
The link should look like this https://drive.google.com/drive/folders/COPY_THIS_PART_HERE_AS_FOLDER_ID?usp=drive_link</br>
where COPY_THIS_PART_HERE_AS_FOLDER_ID is the folder id.</br>
fill in the folder id variable in main.py.</br>

### Step 3
Set up your virtual environment

Make sure you have virtual environment with ``` sudo apt install python3-venv ```</br>
cd to your equivelent of my auto-db-backup directory and type ``` python3 -m venv env ```</br>
activate the venv with ```source venv/bin/activate```</br>
Install pydrive ```pip install PyDrive```</br>
Deactivate the venv ```deactivate```</br>

### Step 4 
Setup a cronjob for your run script to automatically save backups

In the root directory ```crontab -e```</br>
Create a new cronjob similar to this ```0 0 * * * /usr/bin/python3 /usr/local/bin/auto-db-backup/scripts/run.py```</br>
This will run my main script every day at midnight to backup my databases</br>
You can get different scheduling with this website https://crontab.guru</br>

Thats it.
