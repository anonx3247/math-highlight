import re
import sys

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

'''
with open(sys.argv[1]) as f:
    lines = [line for line in f]
    corpus = ""
    for line in lines:
        corpus += line
'''

symb = r"[=$+\-\/*^()_]+"

with open('test') as f:
    lines = [line for line in f]
    corpus = ""
    for line in lines:
        corpus += line
# a variable is defined by a word = numerical-value expression

class Parser:

    def get_vars(self, corpus, symb):
        exps = self.get_exp(corpus, symb)
        decs = [exp for exp in exps if re.search("=", exp.text) != None] 

        def extract(decs):
            extracted = []
            for dec in decs:
                ext = re.split("=", dec.text)
                extracted.append([ext, dec])
            return extracted

        return {ext[0][0]: (ext[0][1], ext[1].span) for ext in extract(decs)}

    def sanitize(self, declaration, symb):
        dec = re.sub(r"\s+", " ", declaration)
        dec = re.sub(r"\s*(" + symb + r")\s*", r"\1", dec)
        return dec

    def get_exp(self, text, symb):
        tokens = tokenize(text, symb)
        return [tok for tok in tokens if self.is_exp(tok, symb)]

    def is_exp(self, tok, symb):
        if re.search(r"((\w+|\d+)" + symb + r")+(\w+|\d+)(\))*", tok.text) != None:
            return True
        else:
            return False

    def tokenize(self, text, symb):
        text = self.sanitize(text, symb)
        return [Token(tok) for tok in self.search_all(r"[^\s]+", text)]

    def search_all(self, reg, text):
        matches = []
        current = 0
        while (match := re.search(reg, text)) is not None:
            _, j = match.span()
            matches.append([match.group(), (match.span()[0]+current, match.span()[1]+current)])
            current += (j+1)
            text = text[j+1:]
        return matches
    def stitch(self, tokens):
        s = ""
        for token in tokens:
            s += token.text
            s += ' '
        return s

    def hl(self, lines, symb):
        def color_line(line):
            tokens = self.tokenize(line, symb)
            colored = []
            for tok in tokens:
                if self.is_exp(tok, symb):
                    new = Token([tok.text, tok.span])
                    new.text = color.RED + new.text + color.END
                    colored.append(new)
                else:
                    colored.append(tok)
            return self.stitch(colored)

        colored_lines = [color_line(line) for line in lines]
        for colored in colored_lines:
            print(colored)

class Value:
    def __init__(self, raw):
        self.val = float(re.sub("[^0-9]*", "", raw))
        self.unit = re.sub("[0-9]*", "", raw)

class Token:
    def __init__(self, match):
        self.span = match[1]
        self.text = match[0]

    def __repr__(self):
        return "'{}' : {}".format(self.text, self.span)

        

    
    