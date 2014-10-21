import click
import os
import shutil as sh
from guessit import guess_file_info
from string import capwords
from .util import *
from . import config

TARGET_DIR = config.config["paths"]["dest"]

def sort_file(db, filename, copy, learn=False):
    # This could obviously be less ridiculous
    g = guess_file_info(os.path.basename(filename))

    try:
        show_name = g["series"]
        ep = g["episodeNumber"]
    except KeyError:
        try:
            show_name = g["title"]
            ep = g["episodeNumber"]
        except KeyError:
            click.secho("Guessit could not parse <{}>".format(filename), fg="red")
            return()

    id_show_name = db.lookup(show_name)
    fuzzed = False
    click.echo(click.style("Sorting {}".format(filename), fg="blue"))
    if id_show_name is None:
        fuzzy_names = db.fuzzy_lookup(show_name)
        if len(fuzzy_names) == 0:
            click.echo(" No fuzzy matches found.")
        elif len(fuzzy_names) == 1:
            id_show_name = fuzzy_names.pop()
            click.echo(click.style(" Fuzzy matched, {} -> {}".format(show_name, id_show_name), fg="yellow"))
            fuzzed = True
        else:
            id_show_name = read_sel(" Multiple fuzzy matches for {}".format(filename), fuzzy_names)
            if id_show_name is not None:
                fuzzed = True
                click.echo(click.style("Fuzzy matched, {} -> {}".format(show_name, id_show_name), fg="yellow"))
    else:
        click.echo(click.style(" Exact matches {} -> {}".format(show_name, id_show_name),fg="green"))

    if id_show_name is None:
        if learn:
            click.echo(click.style(" Show <{}> is not known".format(show_name), fg="blue"))
            sel = click.prompt(" (s)kip [default], (l)earn, (a)lias, (x) learn-as-alias", type=click.Choice(['s', 'l', 'a']))

            if sel == 'l':
                if click.confirm("  Learn show {}".format(show_name)):
                    id_show_name = show_name
                    db.add_show(id_show_name)

            elif sel == 'a':
                parent_name = read_sel("  Please choose a parent to alias {}".format(show_name), db.all_shows)
                if parent_name is not None:
                    if click.confirm("  Learn {} -> {}?".format(show_name, parent_name)):
                        id_show_name = parent_name
                        db.add_alias(id_show_name, show_name)

            elif sel == 'x':
                new_name = click.prompt("  New show name")
                if click.confirm("  Add new show {} with alias {}".format(new_name, show_name)):
                    id_show_name = new_name
                    db.add_show(id_show_name)
                    db.add_alias(show_name, id_show_name)

        else:
            click.echo(click.style(" Skipped {}".format(filename), fg="blue"))
    elif fuzzed:
        if click.confirm(click.style(" Add alias for {} -> {}?".format(show_name, id_show_name), fg="blue", bold=True)):
            db.add_alias(show_name, id_show_name)
        else: id_show_name = None  # If alias was not added, skip sorting

    if id_show_name is not None:
        _, ext = os.path.splitext(filename)
        dest_dir = os.path.join(TARGET_DIR, capwords(id_show_name))
        dest = os.path.join(dest_dir, "{} - {}{}".format(capwords(id_show_name), ep, ext))
        click.echo(click.style(" ┌ Sorting {} -> {}".format(filename, dest), fg="blue"))
        if not os.path.exists(dest_dir):
            click.echo(click.style(" ├ Making target directory: {}".format(dest_dir), fg="yellow"))
            os.mkdir(dest_dir)
        if os.path.exists(dest):
            click.echo(click.style(" ├ Overwriting existing file", fg="yellow"))

        if copy:
            sh.copyfile(filename, dest)
            click.echo(" ├ Copying file...")
        else:
            os.rename(filename, dest)
            click.echo(" ├ Moving file...")

        click.echo(click.style(" └ Done", fg="green"))

