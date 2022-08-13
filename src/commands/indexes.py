import click
import meilisearch.errors

from src.libs import libs
from src.libs import validation
from src.libs import echo
from tabulate import tabulate
import json
import i18n


@click.group(name='indexes')
def indexes():
    """
    management indexes commands (lists|create|delete|destroy)
    """
    pass


@indexes.command()
@click.option('--limit', '-l', default=5, type=int, help="get indexes limit")
def lists(limit):
    """get all indexes information """
    client = libs.c()
    response = client.get_indexes({"limit": limit})
    if len(response['results']) == 0:
        message = i18n.t('message.no_results')
        click.echo(click.style(message, fg='red'))
        return
    disp = {
        "name": [],
        "primary": [],
        "createdAt": [],
        "updatedAt": []
    }
    for ix, dat in enumerate(response['results']):
        disp['name'].append(dat.uid)
        disp['primary'].append(dat.primary_key)
        disp['createdAt'].append(dat.created_at.strftime('%Y/%m/%d %H:%M:%S'))
        disp['updatedAt'].append(dat.updated_at.strftime('%Y/%m/%d %H:%M:%S'))

    print(tabulate(disp, headers='keys'))


@indexes.command()
@click.option(
    '--name',
    '-n',
    type=str,
    required=False,
    help="create index name",
    callback=validation.validate_exists_index_name
)
@click.option('--primary', '-p', type=str, required=False, default="id", help="set primary key optional")
def create(name, primary):
    """create new index """
    message = 'Please enter a new index name'
    color = None
    if name is None:
        check = True
        while check:
            name = click.prompt(click.style(message, fg=color), type=str)
            check = libs.is_exists_index(name)
            color = 'red'
            message = 'Please enter a name that does not exist'

    ret = libs.create_index(name, {
        'primaryKey': primary
    })
    if ret:
        echo.success('Processing completed successfully')


@indexes.command()
@click.option(
    '--name',
    '-n',
    required=False,
    help="delete a index",
    callback=validation.validate_not_exists_index_name)
def delete(name):
    """delete index """
    if name is None:
        name = click.prompt(
            "Please select index",
            type=click.Choice(libs.index_uid_lists()),
            show_default=False
        )
    if libs.delete_index(name):
        echo.success('delete index {} Processing completed successfully'.format(name))


@indexes.command()
@click.option(
    '--index', '-i',
    required=True,
    prompt=True,
    default='',
    type=str,
    help='Specify the index to inspect',
    callback=validation.validate_not_exists_index_name)
def inspect(index):
    """ inspect index"""
    client = libs.c()
    try:
        ret = client.index(index).get_settings()
        echo.info('see reference: https://docs.meilisearch.com/reference/api/settings.html')
        print(json.dumps(ret, indent=4, ensure_ascii=False))
    except meilisearch.errors.MeiliSearchApiError as e:
        echo.error(e)


@indexes.command()
@click.option(
    '--index', '-i',
    required=True,
    prompt=True,
    default='',
    type=str,
    help='setting reset for index',
    callback=validation.validate_not_exists_index_name)
def reset(index):
    """index setting reset"""
    client = libs.c()
    try:
        ret = client.index(index).reset_settings()
        echo.info('see reference: https://docs.meilisearch.com/reference/api/settings.html#reset-settings')
        echo.success('Successfully reset index settings for {}'.format(ret['indexUid']))
    except meilisearch.errors.MeiliSearchApiError as e:
        echo.error(e)


@indexes.command()
@click.option(
    '--index', '-i',
    required=True,
    prompt=True,
    default='',
    type=str,
    help='setting reset for index',
    callback=validation.validate_not_exists_index_name)
@click.option(
    '--file',
    help="import by synonyms (json only)",
    required=False,
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True
    )
)
def synonyms(index, file):
    """setting synonyms in index"""
    echo.info('details see reference: https://docs.meilisearch.com/learn/configuration/synonyms.html')
    if file is None:
        echo.line('Use `--file` to import a synonym file\n{}'.format('----' * 10))
        finish = True
        synonyms_data = {}
        while finish:
            target = click.prompt('please enter target word', type=str)
            words = click.prompt('please enter synonyms word(Separate by `,` if multiple)', type=str)
            synonyms_data[target] = words.split(',')
            if click.confirm('Do you want to set it with the entered value?'):
                finish = False
        request_data = synonyms_data

    else:
        with open(file, 'r') as f:
            json_data = json.load(f)
        request_data = json_data
    try:
        client = libs.c()
        client.index(index).update_synonyms(request_data)
        echo.success('Successfully updated synonym')
    except meilisearch.errors.MeiliSearchApiError:
        echo.error('Api errors')


@indexes.command()
def destroy():
    """
    Delete all indexes
    """
    if click.confirm(click.style('Delete all indexes?', fg='red')):
        indexes_list = libs.index_uid_lists()
        if not indexes_list:
            echo.warning("index does not exist")
            return
        with click.progressbar(indexes_list) as bar:
            for item in bar:
                libs.delete_index(item)
