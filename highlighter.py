# Library used for regular expressions
import re

# Define color codes
# These are special characters used to color characters within a terminal
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

# This defines a regular expression with all the mathematical symbols we allow
symb = r"[=+\-\/*^()_]+"

class Highlighter:
    # Cleans the text by removing excess whitespaces
    def sanitize(self, declaration, symb):
        dec = re.sub(r"\s+", " ", declaration)
        dec = re.sub(r"\s*(" + symb + r")\s*", r"\1", dec)
        return dec

    # tells if the given token is a mathematical expression or not
    def is_exp(self, tok, symb):
        if re.search(r"((\w+|\d+)" + symb + r")+(\w+|\d+)(\))*", tok) != None:
            return True
        else:
            return False

    # transform a string into a list of tokens
    def tokenize(self, text, symb):
        text = self.sanitize(text, symb)
        return [tok for tok in self.search_all(r"[^\s]+", text)]

    # Runs a search for a given regular expression `reg` and returns all matches found
    def search_all(self, reg, text):
        matches = []
        current = 0
        while (match := re.search(reg, text)) is not None:
            _, j = match.span()
            matches.append(match.group())
            current += (j+1)
            text = text[j+1:]
        return matches

    # reconstructs a single string from a list of tokens
    def stitch(self, tokens):
        s = ""
        for token in tokens:
            s += token
            s += ' '
        return s

    # highlights a list of lines and prints out the result
    def hl(self, lines, symb):
        def color_line(line):
            tokens = self.tokenize(line, symb)
            colored = []
            for tok in tokens:
                if self.is_exp(tok, symb):
                    colored.append(color.RED + tok + color.END)
                else:
                    colored.append(tok)
            return self.stitch(colored)

        colored_lines = [color_line(line) for line in lines]
        for colored in colored_lines:
            print(colored)

