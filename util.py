import click
import os
import re

__all__ = ["read_sel", "scan_tree"]

def read_sel(header, options):
    nopt = len(options)
    imax = len(str(len(options)))

    click.echo(click.style(header + "\n", bold=True))

    for i, item in enumerate(options):
        click.echo("  │ {}".format(i + 1).ljust(imax) + " │ {}".format(item))
    click.echo("")
    sel = click.prompt("Please choose (0 to skip)", type=click.IntRange(0, nopt))

    if sel == 0:
        return(None)
    else:
        return(options[sel - 1])

MEDIA_FILES = ["mkv", "mp4", "avi", "m4v"]
MEDIA_PATTERN = re.compile(".*\.(?:{})".format("|".join(MEDIA_FILES)))

def scan_tree(root):
    click.echo(click.style("Scanning folders:", bold=True))
    matches = []
    for root, dirnames, filenames in os.walk(root):
        click.echo("  {}".format(root))
        tmp_match = []
        for filename in filenames:
            if MEDIA_PATTERN.match(filename):
                matches.append(os.path.join(root, filename))
                tmp_match.append(os.path.join(root, filename))
        pretty_print_tree(tmp_match)


    return(matches)

def pretty_print_tree(tree):
    try:
        final = tree.pop()
        for item in tree:
            click.echo("   ├ {}".format(item))
        click.echo("   └ {}".format(final))
    except IndexError:
        click.echo(click.style("   └ None", fg="yellow"))
