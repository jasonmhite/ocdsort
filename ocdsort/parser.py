# coding=UTF-8

# For some reason, Flexget's parser works great for parsing stuff, but
# when I tried to port it with the exact same options it didn't work.

from flexget.plugins.parsers.parser_guessit import ParserGuessit

__all__ = ["parse_episode"]

p = ParserGuessit()

def parse_episode(name):
    r = p.parse(name, "episode", name)

    return({"series": r.series, "episodeNumber": r.episode})
