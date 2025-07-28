import sys

pairs = {
    ')': '(',
    ']': '[',
    '}': '{',
}

def is_opening(symbol):
    return symbol in '([{'

def is_closing(symbol):
    return symbol in ')]}'

def check_balance(expression):
    stack = []

    print(f"Expresión: {expression}")
    print("Pasos de la pila:")

    for char in expression:
        if is_opening(char):
            stack.append(char)
            print(f"  Push: {char} - pila: {stack}")
        elif is_closing(char):
            if len(stack) == 0 or stack[-1] != pairs[char]:
                print(f" Error: se esperaba {pairs[char]} pero no se encontró")
                return False
            print(f"  Pop: {char} . pila antes: {stack}")
            stack.pop()

    if len(stack) == 0:
        print("Se balanceo")
        return True
    else:
        print(f"No se balanceo Pila final: {stack}\n")
        return False

def main():
    try:
        with open("input.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Error: input.txt no encontrado")
        return
    except Exception as e:
        print(f"Error: {e}")
        return

    line_num = 1
    for line in lines:
        line = line.strip()
        if line:  # Skip empty lines
            print(f"Línea {line_num}:")
            check_balance(line)
            line_num += 1

if __name__ == "__main__":
    main()
