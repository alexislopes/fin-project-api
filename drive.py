from pydrive.drive import GoogleDrive
from auth import auth

def drive():
  return GoogleDrive(auth())