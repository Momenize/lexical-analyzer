import re

token_spec = [
    ('NUM',    r'\d+(\.\d*)?'),             
    ('ID',        r'[A-Za-z_][A-Za-z0-9_]*'), 
    ('OP',        r'==|!=|<=|>=|[+\-*/=<>]'), 
    ('DELIM',     r'[(){};,]'),               
    ('NEWLINE',   r'\n'),                     
    ('SKIP',      r'[ \t]+'),                  
    ('COMMENT',   r'#.*'),                   
    ('MISMATCH',  r'.')

]

tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_spec)
get_token = re.compile(tok_regex).match     

def tokenize(code):
    line_num = 1
    pos = 0
    tokens = []

    while pos < len(code):
        match = get_token(code, pos)
        if not match:
            raise RuntimeError(f'Unexpected character {code[pos]!r} on line {line_num}')
        
        kind = match.lastgroup
        value = match.group()
        
        if kind == 'NEWLINE':
            line_num += 1
        elif kind in ('SKIP', 'COMMENT'):
            pass
        elif kind == 'ID' and value in {'if', 'else', 'while', 'return'}:
            tokens.append(('KEYWORD', value))
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Illegal character {value!r} on line {line_num}')
        else:
            tokens.append((kind, value))
        
        pos = match.end()
    
    return tokens

file = open('given_code.txt', 'r')
text = file.read()

tokens = tokenize(text)
for token in tokens:
    print(token)