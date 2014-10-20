import click
import os
import shutil as sh
from guessit import guess_file_info
from string import capwords
from .util import *
from . import config

TARGET_DIR = config.config["paths"]["dest"]

def sort_file(db, filename, copy):
    # This could obviously be less ridiculous
    g = guess_file_info(filename)

    show_name = g["series"]
    ep = g["episodeNumber"]

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

