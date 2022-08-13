import click
import configparser
import os
import meilisearch
from src.libs import echo
import json
APP_NAME = 'minerva'
APP_CONFIG_DIR = click.get_app_dir(APP_NAME)


def c():
    cfg = read_config()
    if cfg['api_key'] == '':
        apikey = None
    else:
        apikey = cfg['api_key']
    client = meilisearch.Client(cfg['host'], api_key=apikey)
    return client


def read_config():
    cfg = os.path.join(APP_CONFIG_DIR, 'config.ini')
    config = configparser.ConfigParser()
    config.read(cfg)
    values = {}
    for key in config['DEFAULT']:
        values[key] = config['DEFAULT'][key]
    return values


def is_exists_config_file():
    cfg = os.path.join(APP_CONFIG_DIR, 'config.ini')
    return os.path.exists(cfg)

def input_config_values():
    host = click.prompt('Please enter a meilisearch host', type=str, default="http://127.0.0.1:7700")
    master_key = click.prompt('Please enter a meilisearch api Master Key', default="")
    return [host, master_key]


def writing_by_config(values, path):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {
        'Host': values[0],
        'Master_Key': values[1],
        'Api_Key': values[2]
    }
    os.makedirs(click.get_app_dir(APP_NAME), exist_ok=True)
    try:
        with open(path, 'w') as f:
            config.write(f)
        click.echo(click.style('Configuration file successfully created!', fg="green"))
    except (FileExistsError, FileNotFoundError):
        click.echo(click.style('Failed to create configuration file', fg="red"))


def is_exists_index(name: str):
    """
    exists index
    :param name:
    :return:
    """
    client = c()
    try:
        client.get_index(name)
        return True
    except meilisearch.errors.MeiliSearchApiError:
        return False


def create_index(name: str, options: dict):
    """
    create index
    :param name:
    :return:
    """
    try:
        client = c()
        client.create_index(name, options)
        return True
    except meilisearch.errors.MeiliSearchApiError:
        click.echo(click.style("Bad Request", fg="red"))
        return False


def index_uid_lists():
    client = c()
    indexs = client.get_indexes({"limit": 100})
    return [dat.uid for i, dat in enumerate(indexs['results'])]


def delete_index(name):
    try:
        client = c()
        client.delete_index(name)
        return True
    except meilisearch.errors.MeiliSearchApiError:
        echo.error('Bad Request')
        return False


def import_file_json(filepath):
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data
    except json.decoder.JSONDecodeError:
        return False

