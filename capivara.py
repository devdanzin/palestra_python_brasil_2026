def max_power(a, b):
    """Encontra o maior número possível na exponenciação de um par."""
    if a > b:
        result = b**a
        if b < 0 and a % 2 == 0:
            result = abs(result)
        return result
    else:
        result = a**b
        if a < 0 and b % 2 == 0:
            result = abs(result)
