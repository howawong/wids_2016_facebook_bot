import requests
#TODO fill in token
# TOKEN = ''
r = requests.post('https://graph.facebook.com/v2.6/me/subscribed_apps?access_token=' + TOKEN)
print r.json()
