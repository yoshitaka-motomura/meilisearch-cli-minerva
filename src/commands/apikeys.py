import click
import meilisearch
import meilisearch.errors
import json
from src.libs import libs
from tabulate import tabulate
import questionary

default_actions = (
    '*',
    'search',
    'documents.add',
    'documents.get',
    'documents.delete',
    'indexes.create',
    'indexes.get',
    'indexes.update',
    'indexes.delete',
    'tasks.get',
    'settings.get',
    'settings.update',
    'stats.get',
    'dumps.create',
    'version',
    'keys.get',
    'keys.create',
    'keys.update',
    'keys.delete'
)


def client():
    cfg = libs.read_config()
    return meilisearch.Client(cfg['host'], api_key=cfg['master_key'])


@click.group(name='keys')
def api_keys():
    """
    manage api keys
    """
    pass


@api_keys.command()
def lists():
    """api keys lists"""
    c = client()
    the_keys = c.get_keys({"limit": 50})
    click.secho("Results. {} api keys".format(the_keys['total']), fg="blue")
    print(tabulate(the_keys['results'], headers='keys'))


@api_keys.command(name="get")
@click.argument('key', required=True)
def get_api_key(key):
    """get api key"""
    c = client()
    try:
        ret = c.get_key(key)
        data = json.dumps(ret, indent=4)
        print(data)
    except meilisearch.errors.MeiliSearchApiError:
        click.secho('meilisearch api errors')
        click.Abort()


@api_keys.command(name="create")
def create_api_key():
    """create api key"""
    name = click.prompt("please enter a new api key name", default='')
    desc = click.prompt("please enter api key description", default='')
    actions = questionary.checkbox(
        "Specify the actions to be assigned to the keys to be created (select * to assign all)",
        choices=default_actions
    ).ask()
    if '*' in actions:
        actions = ['*']
    if click.confirm('Generate a new API KEY? (This API KEY applies to all indexes)'):
        c = client()
        try:
            ret = c.create_key({
                'name': name,
                'description': desc,
                'actions': actions,
                'indexes': ['*'],
                'expiresAt': None
            })
            click.secho('Successfully created API KEY: {}'.format(ret['key']), fg="green")
        except meilisearch.errors.MeiliSearchApiError as e:
            click.secho(e, fg='red')
            return False


@api_keys.command(name="delete")
@click.argument('key', required=True)
def delete_api_key(key):
    """delete api key"""
    cfg = libs.read_config()
    c = client()
    if cfg['api_key'] == key:
        click.secho('currently set API KEY cannot be deleted.', fg="red")
        return
    try:
        c.get_key(key)
        c.delete_key(key)
        click.secho('API KEY has been successfully deleted', fg='green')
    except meilisearch.errors.MeiliSearchApiError:
        click.secho('API key that does not exist.', fg="red")

