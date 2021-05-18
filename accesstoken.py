import requests

client_id = "db7d2120c6da440e9c3347bbfb47b36d"
client_secret = "AVRajcRXxMtk53dX9gjs7YGAdP5M7uQv"

token_url = 'https://us.battle.net/oauth/token'
accessParams = {'grant_type':'client_credentials'}

r = requests.post(token_url, data = accessParams, auth=(client_id, client_secret))
print(r.json()['access_token'])

print("Writing to token.txt...")
f = open("token.txt", "w")
f.write(r.json()['access_token'])
f.close()