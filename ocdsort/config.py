# coding=UTF-8
import yaml
import os
import click

# This is a half-assed config setup and it really doesn't support
# any location for the config file other than default, though some of
# the machinery is here to add it later.

__all__ = ["config", "init_config", "load_config"]

NAME = 'ocdsort'
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
    os.mkdir(CONFIGDIR)
    click.echo("Writing {}".format(DEFAULT_CONFIG_FILE))
    with open(DEFAULT_CONFIG_FILE, 'w') as f:
        f.write(DEFAULT_CONFIG)


def load_config(conf=DEFAULT_CONFIG_FILE):
    with open(conf) as f:
        cfg = f.read()

    return(yaml.load(cfg))

config = load_config()
#try:
    #config = load_config()
#except FileNotFoundError:
    #click.secho("No config file found, initializing at {}".format(CONFIGDIR), fg="red")
    #config = load_config()

if __name__ == "__main__":
    init_default_config()

