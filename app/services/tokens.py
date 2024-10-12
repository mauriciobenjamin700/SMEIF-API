from decouple import config
from fastapi.exceptions import HTTPException
from jose import jwt, JWTError


SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")



def encode_token(data_token: dict) -> str:
    """
    Codifica um dicionário em um token jwt
    
    - dados:

        - cpf: str
        - name: str
        - phone: str
        - phone_optional: str = ""
        - email: str
        - level: int
    
    """
    return jwt.encode(data_token, SECRET_KEY, algorithm=ALGORITHM)

    # Funções abaixo foram usadas para teste. Não sei se iremos precisar decodificar o token ainda no backend, mas caso precisemos, teremos a função a baixo
def decode_token(token: str) -> dict:
    """
    Decodifica um token jwt em um dicionário com seu conteúdo
    
    Chaves do Token:
        - id: str
        - name: str
        - email: str
        - level: str
        - pixkey_type: str
        - pixkey: str
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    except JWTError:

        raise HTTPException(401, "Acesso Negado")
    
    except Exception as e:
        
        raise HTTPException(500, f"Erro no servidor: {e}")
    