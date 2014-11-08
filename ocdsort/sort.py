# coding=UTF=8
import click
import os
import shutil as sh
#from guessit import guess_file_info
from string import capwords
from .util import *
from . import config
from .parsers import ParserGuessit

P = ParserGuessit()

TARGET_DIR = config.config["paths"]["dest"]

def sort_file(db, filename, copy, verb=False, learn=False):
    # This could obviously be less ridiculous
    #g = guess_file_info(os.path.basename(filename), options={"type": "episode"})

    g = P.parse_series(os.path.basename(filename))

    try:
        show_name = g.series
        ep = g.episode
    except KeyError:
        click.secho(INDENT("Guessit could not parse <{}>".format(filename)), fg="red")
        return()

    id_show_name = db.lookup(show_name)
    fuzzed = False
    click.secho(INDENT("Sorting {}".format(filename)), fg="blue")
    with INDENT as I:
        if id_show_name is None:
            fuzzy_names = db.fuzzy_lookup(show_name)
            if len(fuzzy_names) == 0:
                click.echo(I("No fuzzy matches found."))
            elif len(fuzzy_names) == 1:
                id_show_name = fuzzy_names.pop()
                click.secho(I("Fuzzy matched, {} -> {}".format(show_name, id_show_name)), fg="yellow")
                fuzzed = True
            else:
                id_show_name = read_sel(" Multiple fuzzy matches for {}".format(filename), fuzzy_names)
                if id_show_name is not None:
                    fuzzed = True
                    click.secho(I("Fuzzy matched, {} -> {}".format(show_name, id_show_name)), fg="yellow")
        else:
            click.secho(I("Exact matches {} -> {}".format(show_name, id_show_name)),fg="green")

        if id_show_name is None:
            if learn:
                click.secho(I("Show <{}> is not known".format(show_name)), fg="blue")
                sel = click.prompt(I("(s)kip [default], (l)earn, (a)lias, (x) learn-as-alias"), type=click.Choice(['s', 'l', 'a', 'x']), default='s')

                if sel == 'l':
                    with I:
                        if click.confirm(I("Learn show {}".format(show_name))):
                            id_show_name = show_name
                            db.add_show(id_show_name)

                elif sel == 'a':
                    parent_name = read_sel(I("Please choose a parent to alias {}").format(show_name), db.all_shows)
                    if parent_name is not None:
                        with I:
                            if click.confirm(I("Learn {} -> {}?".format(show_name, parent_name))):
                                id_show_name = parent_name
                                db.add_alias(id_show_name, show_name)

                elif sel == 'x':
                    with I:
                        new_name = click.prompt(I("New show name"))
                        if click.confirm(I("Add new show {} with alias {}".format(new_name, show_name))):
                            id_show_name = new_name
                            db.add_show(id_show_name)
                            db.add_alias(show_name, id_show_name)

            else:
                click.secho(I("Skipped {}".format(filename)), fg="blue")
        elif fuzzed:
            if click.secho(I("Add alias for {} -> {}?".format(show_name, id_show_name)), fg="blue", bold=True):
                db.add_alias(show_name, id_show_name)
            else: id_show_name = None  # If alias was not added, skip sorting

        if id_show_name is not None:
            _, ext = os.path.splitext(filename)
            dest_dir = os.path.join(TARGET_DIR, capwords(id_show_name))
            dest = os.path.join(dest_dir, "{} - {}{}".format(capwords(id_show_name), ep, ext))
            click.secho(I("┌ Sorting {} -> {}".format(filename, dest)), fg="blue")
            if not os.path.exists(dest_dir):
                click.secho(I("├ Making target directory: {}".format(dest_dir)), fg="yellow")
                os.mkdir(dest_dir)
            if os.path.exists(dest):
                click.secho(I("├ Overwriting existing file"), fg="yellow")

            if copy:
                sh.copyfile(filename, dest)
                click.echo(I("├ Copying file..."))
            else:
                os.rename(filename, dest)
                click.echo(I("├ Moving file..."))

            click.style(I("└ Done"), fg="green")

