import yaml
import os
import click
from db import init_db

# This is a half-assed config setup and it really doesn't support
# any location for the config file other than default, though some of
# the machinery is here to add it later.

__all__ = ["config", "init_config", "load_config"]

NAME = 'sorter'
DEFAULT = os.path.join(os.environ["HOME"], ".config", NAME)

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
    conf=DEFAULT
)

DEFAULT_CONFIG_FILE = os.path.join(DEFAULT, "config.yml")

try:
    CONFIGDIR = os.path.join(os.environ["XDG_CONFIG_HOME"], NAME)
except KeyError:
    CONFIGDIR = DEFAULT

def init_default_config():
    if os.path.exists(DEFAULT_CONFIG_FILE):
        click.echo(click.style("Default config already file exists at {}".format(CONFIGDIR), fg="red"))
    else:
        os.makedirs(CONFIGDIR)
        click.echo("Writing {}".format(DEFAULT_CONFIG_FILE))
        with open(DEFAULT_CONFIG_FILE, 'w') as f:
            f.write(DEFAULT_CONFIG)

def load_config(conf=DEFAULT_CONFIG_FILE):
    with open(conf) as f:
        cfg = f.read()

    return(yaml.load(cfg))

try:
    config = load_config()
except:
    config = None

if __name__ == "__main__":
    init_default_config()
    init_db(os.path.join(CONFIGDIR, "main.db"))

