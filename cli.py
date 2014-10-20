import click
from db import init_db, Database
from util import *
from sort import sort_file
import os
import config

# Config support could be a lot better
# Maybe a startup() function to load stuff?

TARGET_DIR = config.config["paths"]["dest"]
db = Database(config.config["paths"]["db"])

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
@click.argument("filename", type=click.Path(exists=True))
def scan_and_sort(filename, copy):
    """Recursively scan for media files and sort matched entries."""
    assert os.path.isdir(filename)
    files = scan_tree(filename)
    for filename in files:
        sort_file(db, filename, copy)



cli.add_command(scan_and_sort)

@click.group("list")
def list_group():
    pass

@click.command("shows")
def list_shows():
    click.echo(click.style("Current shows:", fg="blue", bold=True))
    for show in db.all_shows:
        click.echo("  │ {}".format(show))

@click.command("aliases")
def list_aliases():
    click.echo(click.style("Known aliases:", fg="blue", bold=True))
    aliases = db.all_aliases
    parents = [db.get_parent(i) for i in aliases]

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
        click.echo("  {}".format(s))


list_group.add_command(list_shows)
list_group.add_command(list_aliases)
cli.add_command(list_group)

@click.group("add")
def add_new():
    pass

@click.command("show")
@click.option("name", prompt=True)
def add_show(name):
    if click.confirm(click.style("Add show: {}".format(name), fg="blue", bold=True)):
        db.add_show(name)

add_new.add_command(add_show)
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
