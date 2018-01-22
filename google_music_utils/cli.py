# -*- coding: utf-8 -*-

"""Console script for google_music_utils."""

import click
import google_music_utils as gmu


@click.group()
def main(args=None):
    pass


@main.command()
@click.option('--g-from', metavar='from', help='From account to transfer music from', required=True)
@click.option('--from-password', prompt=True, required=True)
@click.option('--g-to', metavar='to', help='To account to transfer music to', required=True)
@click.option('--to-password', prompt=True, required=True)
def transfer(g_from, from_password, g_to, to_password):
    # click.echo("Transferring music play lists from to")
    gmu.transfer(g_from, from_password, g_to, to_password)

@main.command()
@click.option('--account-name', help='Account where playlists need to be deleted', required=True)
@click.option('--password', prompt=True, required=True)
def delete(account_name, password):
    gmu.delete_playlists(account_name, password)

@main.command()
@click.option('--account-name', help='Account where playlists need to be deleted', required=True)
@click.option('--password', prompt=True, required=True)
@click.argument('pl_name', required=True)
def thumbsup(account_name, password, pl_name):
    gmu.thumbs_up_songs(account_name, password, pl_name)


if __name__ == "__main__":
    main()
