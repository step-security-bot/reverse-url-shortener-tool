# Función para convertir un número decimal a base 62
def decimal_to_base62(decimal_num):
    if decimal_num == 0:
        return '0'
    
    base62_digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    result = []
    
    while decimal_num > 0:
        remainder = decimal_num % 62
        result.append(base62_digits[remainder])
        decimal_num //= 62
    
    return ''.join(result[::-1])

# Función para convertir un número en base 62 a decimal
def base62_to_decimal(base62_num):
    base62_digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    decimal_num = 0
    
    for digit in base62_num:
        decimal_num = decimal_num * 62 + base62_digits.index(digit)
    
    return decimal_num

# Ejemplos de uso
decimal_number = 61
base62_number = decimal_to_base62(decimal_number)
print(f"Decimal: {decimal_number} -> Base62: {base62_number}")
