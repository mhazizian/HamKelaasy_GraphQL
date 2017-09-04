import requests
import json


class Fard_API(object):
    def __init__(self):
        self.client_id = "16573"
        self.client_secret = "17171717"
        self.domain = "http://127.0.0.1:8000/"
        self.fard_domain = "http://fard.ir/"

        self.listening_local_url = "signup_on_fard_listening_url/"

        self.signup_url = self.fard_domain + "oauth3/authorize.php" \
               + "?client_id=" + self.client_id \
               + "&redirect_url=" + self.domain\
               + self.listening_local_url

    def connect(self, request):
        request_token = request.GET['request_token']

        r = requests.get(self.fard_domain + "oauth3/getAccessToken.php"
                         + "?request_token=" + request_token
                         + "&client_id=" + self.client_id
                         + "&client_secret=" + self.client_secret)

        respond = json.loads(r.text)

        if not respond['status'] == 200:
            raise Exception(respond['error']['message'])

        self.access_token = respond['data']['access_token']

    def get_data(self, scope=0):
        r = requests.get(self.fard_domain + "oauth3/getData.php"
                         + "?client_id=" + self.client_id
                         + "&client_secret=" + self.client_secret
                         + "&scope=" + str(scope)
                         + "&access_token=" + self.access_token)
        res = json.loads(r.text)
        if not res['status'] == 200:
            raise Exception(res['error']['message'])
        return res['data']
