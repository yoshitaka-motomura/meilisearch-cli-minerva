import click


def success(message):
    click.echo(click.style(message, fg='green'))


def warning(message):
    click.echo(click.style(message, fg='yellow'))


def error(message):
    click.echo(click.style(message, fg='red'))


def info(message):
    click.echo(click.style(message, fg='blue'))


def line(message):
    click.echo(click.style(message, fg=None))
