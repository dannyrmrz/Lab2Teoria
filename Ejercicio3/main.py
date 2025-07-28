#El algoritmo de Shunting Yard, creado por Edsger Dijkstra, convierte expresiones matemáticas de 
#notación infija (como 3 + 4 * 2) a notación postfija o notación polaca inversa (como 3 4 2 * +). 
#Para lograrlo, utiliza una pila de operadores y una lista de salida. Recorre la expresión token 
#por token: si el token es un número, se agrega directamente a la salida; si es un operador, se 
#comparan sus precedencias con los operadores en la pila y se sacan a la salida los de mayor o 
#igual precedencia antes de apilar el nuevo operador; si es un paréntesis izquierdo, se apila, y 
#si es uno derecho, se desapilan operadores hasta encontrar el paréntesis izquierdo correspondiente. 
#Al finalizar, todos los operadores que quedan en la pila se mueven a la salida. De este modo, 
#la expresión se reestructura para ser evaluada fácilmente usando una pila, sin necesidad de 
#paréntesis ni reglas de precedencia.
import re
import sys

precedence = {
    '*': 3,
    '.': 2,
    '|': 1,
}

def is_operator(c):
    return c in "*.|"

def is_left_assoc(op):
    return op != '*'

def expand_escapes(input_str):
    replacements = {
        r'\n': '\n',
        r'\t': '\t',
        r'\{': '{',
        r'\}': '}',
        r'\\': '\\',
    }
    
    result = input_str
    for old, new in replacements.items():
        result = result.replace(old, new)
    return result

def insert_concat_operators(regex):
    result = []
    chars = list(regex)
    escaped = False

    def is_literal(r):
        return r.isalnum() or r == 'ε'

    i = 0
    while i < len(chars):
        c = chars[i]

        if escaped:
            result.extend(['\\', c])
            escaped = False
            i += 1
            continue

        if c == '\\':
            escaped = True
            i += 1
            continue

        result.append(c)

        if i + 1 < len(chars):
            next_char = chars[i + 1]
            if ((is_literal(c) or c in '*)+?')) and (is_literal(next_char) or next_char in '(\\'):
                result.append('.')
        
        i += 1
    
    return ''.join(result)

def handle_extensions(expr):
    output = []
    chars = list(expr)
    escaped = False

    i = 0
    while i < len(chars):
        c = chars[i]

        if escaped:
            output.extend(['\\', c])
            escaped = False
            i += 1
            continue

        if c == '\\':
            escaped = True
            i += 1
            continue

        if (c == '+' or c == '?') and len(output) > 0:
            group = []
            if output[-1] == ')':
                count = 0
                j = len(output) - 1
                while j >= 0:
                    if output[j] == ')':
                        count += 1
                    elif output[j] == '(':
                        count -= 1
                    group.insert(0, output[j])
                    if count == 0:
                        output = output[:j]
                        break
                    j -= 1
            else:
                group = [output[-1]]
                output = output[:-1]

            if c == '+':
                output.extend(['('] + group + [')', '.', '('] + group + [')', '*', '.'])
            elif c == '?':
                output.extend(['('] + group + ['|', 'ε', ')'])
        else:
            output.append(c)
        
        i += 1
    
    return ''.join(output)

def shunting_yard(expr):
    output = []
    stack = []
    steps = []

    chars = list(expr)
    i = 0
    while i < len(chars):
        c = chars[i]

        if c == '\\' and i + 1 < len(chars):
            output.extend(['\\', chars[i + 1]])
            steps.append(f"Escaped char: \\{chars[i + 1]} -> Output: {''.join(output)}")
            i += 2
            continue

        if c.isalnum() or c == 'ε':
            output.append(c)
            steps.append(f"Token {c} -> Output: {''.join(output)}")
        elif c == '(':
            stack.append(c)
            steps.append(f"Push '(' -> Stack: {''.join(stack)}")
        elif c == ')':
            while len(stack) > 0 and stack[-1] != '(':
                op = stack.pop()
                output.append(op)
                steps.append(f"Pop {op} -> Output: {''.join(output)}")
            if len(stack) > 0 and stack[-1] == '(':
                stack.pop()
        elif is_operator(c):
            while len(stack) > 0:
                top = stack[-1]
                if (is_operator(top) and 
                    ((is_left_assoc(c) and precedence[c] <= precedence[top]) or 
                     (not is_left_assoc(c) and precedence[c] < precedence[top]))):
                    stack.pop()
                    output.append(top)
                    steps.append(f"Pop {top} -> Output: {''.join(output)}")
                else:
                    break
            stack.append(c)
            steps.append(f"Push {c} -> Stack: {''.join(stack)}")
        
        i += 1

    while len(stack) > 0:
        output.append(stack.pop())
        steps.append(f"Flush Stack -> Output: {''.join(output)}")

    return ''.join(output), steps

def main():
    try:
        with open("input.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Error abriendo archivo: input.txt no encontrado")
        sys.exit(1)
    except Exception as e:
        print(f"Error abriendo archivo: {e}")
        sys.exit(1)

    line_number = 1
    for line in lines:
        raw = line.strip()
        if not raw:  # Skip empty lines
            continue
            
        print(f'Expresión original ({line_number}): "{raw}"')

        expanded = expand_escapes(raw)
        preprocessed = insert_concat_operators(handle_extensions(expanded))

        print(f"Preprocesada: {preprocessed}")

        postfix, steps = shunting_yard(preprocessed)
        print(f"Resultado postfix: {postfix}")
        print("Pasos:")
        for step in steps:
            print(f" - {step}")
        print("-" * 40)
        line_number += 1

if __name__ == "__main__":
    main()
