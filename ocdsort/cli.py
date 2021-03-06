# coding=UTF-8
import sys
import os

#  Setup the indentation level so that it's available everywhere
from .util.indent import Indent

__builtins__["INDENT"] = Indent()

try:
    if sys.argv[1] == "init":
        from .schema import init_db
        NAME = "ocdsort"
        CONFDIR = os.path.join(os.environ["HOME"], ".config", NAME)
        os.makedirs(CONFDIR)
        DEFAULT_CONFIG = \
        """---
        settings:
            media_extensions:
                - mkv
                - mp4
                - m4v
                - avi
        paths:
            dest: {dest}
            db: {conf}/main.db
        """.format(
            dest=os.path.join(os.environ["HOME"], "Anime"),
            conf=CONFDIR
        )
        with open(os.path.join(CONFDIR, "config.yml"), 'w') as f:
            f.write(DEFAULT_CONFIG)

        init_db(os.path.join(CONFDIR, "main.db"))

        sys.exit(0)
except IndexError:
    pass

import click
from .db import ShowDB
from .util import *
from .sort import sort_file
from . import config

# Config support could be a lot better
# Maybe a startup() function to load stuff?

TARGET_DIR = config.config["paths"]["dest"]
db = ShowDB(config.config["paths"]["db"])

@click.group()
def cli():
    """Sort shows"""

@click.command("sort")
@click.argument("filename", type=click.Path(exists=True))
@click.option("--copy", is_flag=True)
def do_sort(filename, copy):
    sort_file(db, filename, copy)

cli.add_command(do_sort)

@click.command("scan")
@click.option("--copy", is_flag=True)
@click.option("--learn", is_flag=True)
@click.option("--verbose", is_flag=True)
@click.argument("filename", type=click.Path(exists=True))
def scan_and_sort(filename, copy, verbose, learn):
    """Recursively scan for media files and sort matched entries."""
    assert os.path.isdir(filename)
    files = scan_tree(filename)
    for filename in files:
        sort_file(db, filename, copy, verbose, learn)



cli.add_command(scan_and_sort)

@click.group("list")
def list_group():
    pass

@click.command("shows")
def list_shows():
    click.echo(click.style(INDENT("Current shows:"), fg="blue", bold=True))
    for show in db.all_shows:
        with INDENT as I:
            click.echo(I("│ {}".format(show)))

@click.command("aliases")
def list_aliases():
    click.echo(click.style(I("Known aliases:"), fg="blue", bold=True))
    aliases = db.all_aliases
    parents = [db.lookup(i) for i in aliases]

    maxlen = max([len(i) for i in parents]) - 1
    padnames = [s.ljust(maxlen) for s in parents]

    all_matches = dict()
    for (p, a) in zip(padnames, aliases):
        if p != a:
            if p in all_matches:
                all_matches[p].append(a)
            else:
                all_matches[p] = [a]

    sstring = ["│ {}│ {}".format(s, " • ".join(a)) for (s, a) in all_matches.items()]
    for s in sorted(sstring):
        with INDENT as I:
            click.echo(I("{}".format(s)))


list_group.add_command(list_shows)
list_group.add_command(list_aliases)
cli.add_command(list_group)

@click.group("add")
def add_new():
    pass

@click.command("show")
@click.option("--name", prompt=True)
def add_show(name):
    if click.confirm(click.style("Add show: {}".format(name), fg="blue", bold=True)):
        db.add_show(name)

@click.command("alias")
@click.option("--name", prompt=True)
@click.option("--to", type=click.Choice(db.all_shows))
def add_alias(name, to):
    if to is None:
        all_shows = db.all_shows
        to_alias = read_sel("Please select a target to alias:", all_shows)
    else:
        to_alias = name

    if to_alias is not None:
        if click.confirm(click.style("Alias {} -> {}".format(to_alias, name))):
            db.add_alias(to_alias, name)

add_new.add_command(add_show)
add_new.add_command(add_alias)
cli.add_command(add_new)

@click.group("delete")
def delete():
    pass

@click.command("show")
@click.option("--name", type=click.Choice(db.all_shows))
def delete_show(name):
    if name is None:
        all_shows = db.all_shows
        to_delete = read_sel("Please select a show to delete:", all_shows)
    else:
        to_delete = name
    # TODO: Validate the name?

    if to_delete is not None:
        if click.confirm(click.style("Will delete: {}".format(to_delete), fg="red", bold=True)):
            db.delete_show(to_delete)

@click.command("alias")
@click.option("--name", type=click.Choice(db.all_aliases))
def delete_alias(name):
    if name is None:
        all_aliases = set(db.all_aliases)
        all_names = set(db.all_shows)

        aliases = list(all_aliases - all_aliases.intersection(all_names))
        to_delete = read_sel("Please select an alias to delete:", aliases)
    else:
        # TODO: Validate name?
        to_delete = name

    if to_delete is not None:
        if click.confirm(click.style("Will delete: {}".format(to_delete), fg="red", bold=True)):
            db.delete_alias(to_delete)

cli.add_command(delete)
delete.add_command(delete_show)
delete.add_command(delete_alias)

if __name__ == "__main__":
    cli()
