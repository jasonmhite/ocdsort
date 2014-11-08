from click import wrap_text

## The CLI will import this into builtins, so it has to be imported on
# its own

class Indent(object):
    def __init__(self, indent_char="  ", initial_indent=0, max_width=78):
        self._ilevel = initial_indent
        self._indent_char = indent_char
        self._max_width = max_width

    def indenter(self, s):
        indent = self._ilevel * self._indent_char
        indent2 = indent + self._indent_char
        new_s = wrap_text(
            s,
            width=self._max_width,
            initial_indent=indent,
            subsequent_indent=indent2,
        )
        return(new_s)

    def __enter__(self):
        self._ilevel += 1
        return(self.indenter)

    def __exit__(self, type, value, tb):
        self._ilevel -= 1
