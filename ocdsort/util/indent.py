from click import wrap_text

## The CLI will import this into builtins, so it has to be imported on
# its own

class IndentState(object):
    def __init__(self):
        self._state = []

    def __iadd__(self, other):
        self._state.append(other)
        return(self)

    @property
    def as_string(self):
        return("".join(self._state))

    @property
    def extra_indent(self):
        return(self.as_string + self._state[-1])

    @property
    def level(self):
        return(len(self._state))

    def __str__(self):
        return(self.as_string)

    def pop(self):
        self._state.pop()


class Indent(object):

    def __init__(self, indent_char="  ", initial_indent=0, max_width=78):
        self._indent_char = indent_char
        self._max_width = max_width

        self._indent_string = IndentState()
        for i in range(initial_indent):
            self._indent_string += self._indent_char

    def __call__(self, s):
        new_s = wrap_text(
            s,
            width=self._max_width,
            initial_indent=self._indent_string.as_string,
            subsequent_indent=self._indent_string.extra_indent,
        )
        return(new_s)

    def __enter__(self, local_indent=None):
        i = (self._indent_char if local_indent is None else local_indent)
        self._indent_string += i
        return(self)

    def __exit__(self, type, value, tb):
        self._indent_string.pop()
