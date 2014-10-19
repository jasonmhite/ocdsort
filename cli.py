import click
from db import init_db, Database

from sort import sort_file

TARGET_DIR = "/home/jmhite/Anime"

db = Database("./test.db")

@click.group()
def cli():
    """Sort shows"""

@click.command("init")
@click.argument("database_name")
def init(database_name):
    """Initializes default database and config file"""
    click.echo("Building new database: {}".format(database_name))
    init_db(database_name)

cli.add_command(init)

@click.command("sort")
@click.argument("filename", type=click.Path(exists=True))
@click.option("--copy", is_flag=True)
def do_sort(filename, copy):
    sort_file(db, filename, copy)

cli.add_command(do_sort)

@click.command("scan")

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
    for p, a in zip(padnames, aliases):
        if p != a:
            if p in all_matches:
                all_matches[p].append(a)
            else:
                all_matches[p] = [a]

    sstring = ["│ {}│ {}".format(s, ", ".join(a)) for (s, a) in all_matches.items()]
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
    click.echo(click.style("Add show: {}".format(name), fg="blue", bold=True))
    if read_yn():
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
        sel = read_sel("Please select a show to delete:", all_shows)
        if sel is not None:
            to_delete = all_shows[sel]
        else: to_delete = None
    else:
        to_delete = name

    if to_delete is not None:
        click.echo(click.style("Will delete: {}".format(to_delete), fg="red", bold=True))
        if read_yn():
            db.delete_show(to_delete)

@click.command("alias")
@click.option("--name", type=click.Choice(db.all_aliases))
def delete_alias(name):
    if name is None:
        all_aliases = db.all_aliases
        sel = read_sel("Please select an alias to delete:", all_aliases)
        if sel is not None:
            to_delete = all_aliases[sel]
        else: to_delete = None
    else:
        to_delete = name

    if to_delete is not None:
        click.echo(click.style("Will delete: ".format(to_delete), fg="red", bold=True))
        if read_yn():
            db.delete_alias(to_delete)

cli.add_command(delete)
delete.add_command(delete_show)
delete.add_command(delete_alias)


# Replace with click.prompt()
def read_sel(heading, choices):
    sel = None
    click.echo(click.style(heading + "\n", fg="blue", bold=True))
    imax = len(str(len(choices)))
    for (i, item) in enumerate(choices):
        click.echo("  │ {}".format(i).ljust(imax) + " │ {}".format(item))
    click.echo("")

    while True:
        sel = input("choice (q to skip): ")
        if sel == "q":
            sel = None
            break
        elif sel.isdigit():
            try:
                sel = int(sel)
                if sel in range(len(choices)):
                    break
            except:
                continue
        else:
            continue

    return(sel)

# replace with click.confirm()
def read_yn():
    sel = None
    while True:
        sel = input("confirm (y/n): ")
        if sel == "y":
            return(True)
        elif sel == "n":
            return(False)

if __name__ == "__main__":
    cli()
