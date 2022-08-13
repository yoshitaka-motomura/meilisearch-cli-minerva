import click
from src.libs import echo
from src.libs import libs, resource
from meilisearch import errors
import tabulate
import json

resource = resource.Resource()


@click.command(name='search')
@click.option('--index', '-i', default="", type=str, help="search target index")
@click.option('--query', '-q', default="", type=str, help="search query")
@click.option('--limit', '-l', default=25, type=int, help="limit value default:25")
@click.option('--offset', '-o', default=0, type=int, help="offset value default:0")
def search(index, query, limit, offset):
    """search documents"""
    if not libs.is_exists_config_file():
        echo.warning('Please configure the application settings\n`minerva config setup`')
        return
    if index == '':
        index = click.prompt('search target index?')
    if query == '':
        query = ''
    try:
        d = resource.client.index(index).search(query, {
            "limit": limit,
            "offset": offset,
            "attributesToHighlight": ['*']
        })
        info = {
            'query': [d['query']],
            'estimatedTotalHits': [d['estimatedTotalHits']],
            'processingTimeMs': [d['processingTimeMs']],
            'limit': [limit]
        }
        print(tabulate.tabulate(info, headers='keys'))
        print('\nHits. {}'.format("-----"*20))
        print(json.dumps(d['hits'], indent=2, ensure_ascii=False))
        print("-----" * 25)
    except errors.MeiliSearchApiError as e:
        echo.error(e)
