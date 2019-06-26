#!/usr/bin/env python3
import importlib

import click


@click.group()
@click.help_option()
def worker():
    """Workers management commands"""


@worker.command()
@click.option('--name', type=click.Choice(["publisher", "watcher"]), required=True)
def start(name):
    """Starts corresponding worker"""
    module = importlib.import_module("src.workers.%s" % name)
    module.startup()


if __name__ == '__main__':
    worker()
