import guessit
from guessit.plugins.transformers import Transformer, add_transformer
from guessit.containers import PropertiesContainer, NoValidator
from guessit.matcher import GuessFinder
import ABC

# Parsers loosely based on how Flexget passes options to guessit

class Parser(object):
    __metaclass__ = ABC.ABCMeta

    @ABC.abstractmethod
    def parse(self, name):
        raise(NotImplementedError)

def clean_value(name):
    # Move anything in leading brackets to the end
    #name = re.sub(r'^\[(.*?)\](.*)', r'\2 \1', name)

    for char in '[]()_,.':
        name = name.replace(char, ' ')

    # if there are no spaces
    if name.find(' ') == -1:
        name = name.replace('-', ' ')

    # remove unwanted words (imax, ..)
    #self.remove_words(data, self.remove)

    #MovieParser.strip_spaces
    name = ' '.join(name.split())
    return name

class GuessRegexpId(Transformer):
    def __init__(self):
        Transformer.__init__(self, 21)

    def supported_properties(self):
        return ['regexpId']

    def guess_regexps_id(self, string, node=None, options=None):
        container = PropertiesContainer(enhance=False, canonical_from_pattern=False)
        for regexp in options.get("id_regexps"):
            container.register_property('regexpId', regexp, confidence=1.0, validator=NoValidator())
        found = container.find_properties(string, node, options)
        return container.as_guess(found, string)

    def should_process(self, mtree, options=None):
        return options and options.get("id_regexps")

    def process(self, mtree, options=None):
        GuessFinder(self.guess_regexps_id, None, self.log, options).process_nodes(mtree.unidentified_leaves())

add_transformer('guess_regexp_id = ocdsort.parser:GuessRegexpId')
guessit.default_options = {
    'name_only': True,
    'clean_function': clean_value,
}

class GuessitParser(Parser):
    _guess_options = {"type": "episode", "episode_prefer_number": True}

    # This is borrowed directly from Flexget

    def parse(self, name):
        r = guessit.guess_file_info(name, self._guess_options)
        return(r)
