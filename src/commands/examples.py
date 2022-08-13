import click
from src.libs import echo
import os
from pathlib import Path
import shutil


@click.command(name='example')
def example():
    """Output files for building meilisearch via docker-compose"""
    echo.info('output docker-compose file to build meilisearch locally.')
    app_dir = os.path.abspath(os.path.join(Path(__file__).parent, '../'))
    me_dir = os.path.join(os.getcwd(), 'meilisearch')
    if click.confirm('Create a new `meilisearch` directory at the current path location'):
        me_dir = os.path.join(os.getcwd(), 'meilisearch')
        os.makedirs(me_dir, exist_ok=True)
        if not os.path.exists(me_dir):
            echo.error('Either permissions are missing or the directory already exists.')
            return
    else:
        return
    origin = os.path.join(app_dir, 'data', 'docker-compose.yml')
    shutil.copyfile(origin, os.path.join(me_dir, 'docker-compose.yml'))
    echo.line('==' * 40)
    echo.line('STEP 1: cd {}'.format(me_dir))
    echo.line('STEP 2: docker-compose up -d')
    echo.line('STEP 3: minerva config setup')
    echo.success('Please enter `http://127.0.0.1` in the host field\n'
                 'Please enter `MASTER_KEY` in the master key field')
