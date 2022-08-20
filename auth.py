from pydrive.auth import GoogleAuth

def auth():
  gauth = GoogleAuth()
  gauth.LocalWebserverAuth()
  gauth.SaveCredentialsFile('./cred.json')
  return gauth

