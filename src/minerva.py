import click
from tabulate import tabulate
from src.libs import resource
from src.commands import indexes, documents, apikeys, configure, search, examples
import os
import i18n

resource = resource.Resource()


def init_translation():
    path_to_locale_dir = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '../locales'
        )
    )
    i18n.load_path.append(path_to_locale_dir)
    i18n.set("file_format", "json")
    i18n.set("locale", "ja")
    i18n.set("fallback", "ja")
    i18n.set("skip_locale_root_data", True)

@click.group()
def cli():
    """meilisearch cli"""
    pass


@click.command()
def health():
    """
    health check at meilisearch
    """
    ret = resource.health()
    if not ret:
        click.secho('Unable to connect', fg="red")
        return
    message = i18n.t('message.'+ret['status'])
    click.secho('{}'.format(message), fg="green")


@click.command()
def tasks():
    """Meilisearch get tasks"""
    ret = resource.client.get_tasks()
    if len(ret['results']) == 0:
        message = i18n.t('message.nothing_tasks')
        click.secho(message, fg="yellow")
        return
    print(tabulate(ret['results'], headers='keys'))


@click.command()
def versions():
    ret = resource.client.get_version()
    msg = i18n.t('message.version')
    print("Meilisearch {}: {}".format(msg, ret['pkgVersion']))


init_translation()
cli.add_command(configure.configure)
cli.add_command(apikeys.api_keys)
cli.add_command(indexes.indexes)
cli.add_command(documents.documents)
cli.add_command(search.search)
cli.add_command(examples.example)
cli.add_command(tasks)
cli.add_command(health)
cli.add_command(versions)
