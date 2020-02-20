import os
from urllib.parse import parse_qsl

import requests
from requests_oauthlib import OAuth1


"""
Documentación completa sobre el uso y manejo del API de Twitter está disponible en
https://developer.twitter.com/
"""


# Estos key puede obtenerse desde el registro de aplicación en Twitter
oauth_consumer_token = api_key = os.environ.get("TWITTER_API_KEY")
oauth_consumer_secret = api_secret_key = os.environ.get("TWITTER_API_SECRET")

# Estos "access tokens" son oauth tokens válidos para interactuar con Twitter
# Se muestran una sola vez en el registro de la aplicación.
# Si los usamos, podemos saltarnos el resto del los pasos de autenticación con nuestro usuario.
oauth_token = access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
oauth_token_secret = access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN")


# Endpoints para autenticación con OAuth1a
# https://developer.twitter.com/en/docs/basics/authentication/oauth-1-0a
request_token_url = "https://api.twitter.com/oauth/request_token"
access_token_url = "https://api.twitter.com/oauth/access_token"
authorize_url = "https://api.twitter.com/oauth/authorize"

# Algunos endpoints para interactuar con el API (update, delete, detail, and timeline)
# https://developer.twitter.com/en/docs/tweets/post-and-engage/api-reference/post-statuses-update
update_url = "https://api.twitter.com/1.1/statuses/update.json"  #  params: {"status": "str", "in_reply_to_status_id": "str", }
destroy_url = "https://api.twitter.com/1.1/statuses/destroy/{}.json"  #  format id
detail_url =  "https://api.twitter.com/1.1/statuses/show.json"   #  params: {"id": int}
timeline_url = "https://api.twitter.com/1.1/statuses/home_timeline.json" #  params: {"count": 5}


# auth = OAuth1(api_key, api_secret_key, access_token, access_token_secret)
auth = OAuth1(api_key, api_secret_key, None, None)
client = requests.Session()
client.auth = auth

# Se obtienen tokens temporales con un callback oob
resp = client.post(request_token_url, params={'oauth_callback':'oob'})
tmp_tokens = dict(parse_qsl(resp.content.decode('utf-8')))

# Usando los tokens temporales, se obtiene un parámetro oauth_verifier.
# Debe imprimirse `resp.url` para obtener el valor de este parámetro.
resp = client.get(authorize_url, params={"oauth_token": tmp_tokens['oauth_token']})
oauth_verifier = ""  # Get oauth verifier from twitter

# Se obtienen los tokens definitivos para interactuar con el API
resp = client.post(access_token_url, params={"oauth_token":tmp_tokens['oauth_token'], 'oauth_verifier':oauth_verifier})
tokens = dict(parse_qsl(resp.content.decode('utf-8')))

# Se actualiza el método de autenticación del cliente con los nuevos tokens recibidos
client.auth = OAuth1(oauth_consumer_token, oauth_consumer_secret, tokens['oauth_token'], tokens['oauth_token_secret'])

# Ya podemos interactuar con el API de Twitter
resp = client.post(update_url, {"status":"PyMX :)"})
print(resp)


