import os
import requests
import json


class HaloService:
    api_key = os.environ.get('HALO_API_KEY')
    domain = os.environ.get('HALO_API_URL')

    def __init__(self):
        self.default_headers = {'Ocp-Apim-Subscription-Key': HaloService.api_key}

    def get_designations(self):
        return self.decode_response(
            requests.get(f'{self.domain}/metadata/h5/metadata/csr-designations', headers=self.default_headers))

    def get_seasons(self):
        return self.decode_response(requests.get(f'{self.domain}/metadata/h5/metadata/seasons',
                                    headers=self.default_headers))

    def get_top_players(self, season, playlist):
        return self.decode_response(requests.get(f'{self.domain}/stats/h5/player-leaderboards/csr/{season}/{playlist}',
                                                 headers=self.default_headers))

    def decode_response(self, response):
        try:
            return json.loads(response.text)
        except (json.JSONDecodeError, TypeError) as e:
            return None
