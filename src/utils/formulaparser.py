from lark import Lark

def parse_formula(text: str):

    # 単純なパーサーの定義
    grammar = '''
        start       : exp | WORD | or_exp | and_exp | br_exp
        exp         : WORD | or_exp | and_exp | br_exp
        or_exp      : or_exp "|" or_exp | and_exp | br_exp
        and_exp     : and_exp "&" and_exp | br_exp
        br_exp      : "(" exp ")" | WORD
      
        %import common.WORD   // imports from terminal library
        %ignore " "           // Disregard spaces in text
    '''


    # 文字列のパース
    def parse_parentheses(s):
        parser = Lark(grammar, start='start')
        return parser.parse(s)

    parsed = parse_parentheses(text)
    print(parsed.pretty())
    print(parsed)
    return parsed
if __name__ == '__main__':
    parse_formula("(A & B) | C")
    parse_formula("A & (B | C)")
    parse_formula("A & B | C")
    parse_formula("A | B | C")
    parse_formula("A & B & C")