import click
import meilisearch
import meilisearch.errors
from pathlib import Path
from src.libs import echo
from src.libs import libs, resource

resource = resource.Resource()


@click.group(name='documents')
def documents():
    """manage documents"""
    pass


@documents.command(name="import")
@click.argument(
    'file',
    required=True,
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True
    )
)
@click.option(
    '--relative',
    '-r',
    type=bool,
    default=True,
    help='Option to determine the index relative to the file name'
)
def file_import(file, relative):
    """file import json file only"""
    if not libs.is_exists_config_file():
        echo.warning('Please configure the application settings\n`minerva config setup`')
        return
    index_name = Path(file).stem
    if not relative:
        index_name = click.prompt('Do What index import into?', default=index_name)

    data = libs.import_file_json(file)
    if not data:
        echo.error('Failed to load file. should be a JSON file')
        return
    try:
        resource.client.index(index_name).add_documents(data)
        echo.success('Document imported successfully. processing check command `minerva tasks`')
    except meilisearch.errors.MeiliSearchApiError as e:
        echo.error('Failed to import document {}'.format(e))
