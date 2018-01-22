# -*- coding: utf-8 -*-

"""Main module."""
import click
from gmusicapi import Mobileclient
import pyjq


class NotLoggedIn(Exception):
    pass

def gapi(account_name, password):
    # https://github.com/simon-weber/gmusicapi/issues/584
    api = Mobileclient(debug_logging=True, validate=True, verify_ssl=True)
    if not api.login(account_name, password, u'3a033d4d5bb6731d'):
        raise NotLoggedIn("Failed to log into %s" % account_name)

    return api

def transfer(g_from, from_password, g_to, to_password):
    from_api = gapi(g_from, from_password)
    from_play_lists = pyjq.all('.[] | {name: .name, tracks: [.tracks[].trackId]}',
                               from_api.get_all_user_playlist_contents())
    from_api.logout()

    to_api = gapi(g_to, to_password)
    to_play_lists = pyjq.all('.[] | {name: .name, id: .id, tracks: [.tracks[].trackId]}',
                             to_api.get_all_user_playlist_contents())

    def _get_or_create_playlist(pl_name_to_create):
        pl = next(pl for pl in to_play_lists if pl.get("name") == pl_name_to_create) if to_play_lists else None
        if not pl:
            id = to_api.create_playlist(pl_name_to_create)
        else:
            id = pl["id"]

        return id, pl["tracks"] if pl else []

    for pl in from_play_lists:
        pl_id, to_tracks = _get_or_create_playlist(pl["name"])
        tracks_to_add = list(set(pl["tracks"]) - set(to_tracks))
        if tracks_to_add:
            to_api.add_songs_to_playlist(pl_id, tracks_to_add)

    to_api.logout()

def delete_playlists(account_name, password):
    api = gapi(account_name, password)

    for pl in api.get_all_playlists():
        api.delete_playlist(pl["id"])

    api.logout()

def thumbs_up_songs(account_name, password, pl_name):
    api = gapi(account_name, password)

    play_lists = api.get_all_user_playlist_contents()
    pl = next(pl for pl in play_lists if pl.get("name") == pl_name) if play_lists else None

    songs = [{"id": track["trackId"]} for track in pl["tracks"]]

    api.rate_songs(songs, 5)

