import click
from src.libs import echo
from src.libs import libs
from tabulate import tabulate
import meilisearch
import meilisearch.errors
import os

APP_NAME = 'minerva'


@click.group(name='config')
def configure():
    """
    application setup configure
    """
    pass


@configure.command()
def setup():
    echo.info('application setup configure')
    values = libs.input_config_values()
    conf = {
        "host": [values[0]],
        "master key": [values[1]]
    }
    print(tabulate(conf, headers='keys'))
    if click.confirm("Do you want to create a configuration file?"):
        meilisearch_make_apikey(values)


def meilisearch_make_apikey(values):
    cfg = os.path.join(click.get_app_dir(APP_NAME), 'config.ini')
    try:
        client = meilisearch.Client(values[0], api_key=values[1])
        items = client.get_keys({"limit": 100})
        for item in items['results']:
            if item['name'] != 'Default Admin API Key':
                continue
            values.append(item['key'])
            break
        libs.writing_by_config(values, cfg)
    except meilisearch.errors.MeiliSearchApiError:
        src.libs.echo.error('Error create apikey')
        raise click.Abort()
