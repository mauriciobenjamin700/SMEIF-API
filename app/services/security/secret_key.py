import secrets

def generate_secret_key(length: int = 64) -> str:
    """
    Gera uma chave secreta segura.
    
    - Args:
        - length: O comprimento da chave secreta. O padrão é 64 caracteres.
    
    - Returns:
        - str: A chave secreta gerada.
    """
    return secrets.token_hex(length)

if __name__ == "__main__":

    secret_key = generate_secret_key()
    print(f"Chave secreta gerada: {secret_key}")