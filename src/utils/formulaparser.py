from lark import Lark, Tree

def parse_formula(text: str):

    # 検索条件パーサーの定義
    grammar = r'''
    ?start: expr1
    // expression
    ?expr1: expr2
        | or_expr
    or_expr: expr1 "|" expr2

    ?expr2: expr3
        | and_expr
    and_expr: expr2 "&" expr3

    ?expr3: expr4
        | not_expr
    not_expr: "!" expr3

    ?expr4: word
        | priority
    ?priority: "(" expr1 ")"

    word: WORD | SIGNED_NUMBER| w2
    ?w2: /[^\W\d_]+/
    %import common.WORD   // imports from terminal library
    %import common.SIGNED_NUMBER   // imports from terminal library
    %ignore " "           // Disregard spaces in text
    '''


    # 文字列のパース
    def parse_parentheses(s):
        parser = Lark(grammar, start='start')
        return parser.parse(s)

    parsed = parse_parentheses(text)
    # print('=================')
    # print(text)
    # print(parsed.pretty())
    # print(parsed)
    return parsed



def tree_to_str(parsed: Tree):
    match parsed.data:
        case "and_expr":
            expr1 = tree_to_str(parsed.children[0])
            expr2 = tree_to_str(parsed.children[1])
            return f"({expr1}かつ{expr2})"
        case "or_expr":
            # print(parsed)
            expr1 = tree_to_str(parsed.children[0])
            expr2 = tree_to_str(parsed.children[1])
            return f"({expr1}または{expr2})"
        case "word":
            return parsed.children[0].value
        case "not_expr":
            expr1 = tree_to_str(parsed.children[0])
            return f"({expr1}を含まず)"
        case _:
            raise parsed.data

if __name__ == '__main__':
    print(tree_to_str(parse_formula(u"上野")))
    print(tree_to_str(parse_formula("(!A & B) | C")))
    # parse_formula("A & (B | C)")
    # parse_formula("A & B | C")
    # parse_formula("A | B | C")
    # parse_formula("A & !B & C")
    # parse_formula("A & B | C")
    # parse_formula("A | B & C")
    # parse_formula("A & B | C & D")
    # parse_formula("A | B & !C | D")
    # parse_formula("!D")
    # parse_formula("!!D")