from pydrive.auth import GoogleAuth

def auth():
  gauth = GoogleAuth("./settings.yaml")
  gauth.LocalWebserverAuth()
  gauth.SaveCredentialsFile('./cred.json')
  return gauth

