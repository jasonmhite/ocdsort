import click

__all__ = ["read_sel"]

def read_sel(options):
    nopt = len(options)
    imax = len(str(len(options)))

    for i, item in enumerate(options):
        click.echo("  │ {}".format(i + 1).ljust(imax) + " │ {}".format(item))
    sel = click.prompt("Please choose (0 to skip)", type=click.IntRange(0, nopt))
    if sel == 0:
        return(None)
    else:
        return(options[sel - 1])
