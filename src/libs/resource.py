import meilisearch
import meilisearch.errors
from src.libs import libs


class Resource:
    client=None

    def __init__(self):
        try:
            cfg = libs.read_config()
            default_values = {
                'host': 'http://127.0.0.1:7700',
                'api_key': None
            }
            if cfg['api_key'] != '':
                default_values['api_key'] = cfg['api_key']
            self.client = meilisearch.Client(cfg['host'], api_key=default_values['api_key'])
        except KeyError:
            return

    def health(self):
        """
        health check
        :return:
        """
        try:
            _h = self.client.health()
            return _h
        except (meilisearch.errors.MeiliSearchApiError,
                meilisearch.errors.MeiliSearchTimeoutError):
            return False

