from passlib.context import CryptContext


crypt_context = CryptContext(schemes=['sha256_crypt'])


def crypto(value: str) -> str:
    """
    Codifica (hashea) um valor
    
    - Args:
        - value: O valor a ser hasheado.
    
    - Returns:
        - str: O valor hasheado.
    """
    return crypt_context.hash(value)

def verify(value: str, hashed_value: str) -> bool:
    """
    Verifica se um valor corresponde ao hash fornecido.
    
    - Args:
        - value: O valor original.
        - hashed_value: O valor hasheado.
    
    - Returns:
        - bool: True se o valor corresponder ao hash, False caso contrário.
    """
    return crypt_context.verify(value, hashed_value)