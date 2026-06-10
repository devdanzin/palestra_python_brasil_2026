def max_pow(a, b) -> int:
    """Encontra o maior número possível na exponenciação de um par de números."""
    if a > b:
        result = b**a
        if b < 0 and a % 2 == 0:
            result = abs(result)
        print(result)
        return result
    result = a**b
    if a < 0 and b % 2 == 0:
        result = abs(result)
    print(result)
