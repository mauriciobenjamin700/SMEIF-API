"""
- base_validation
- validate_string_field
- validate_cpf
- validade_email
- validate_date
- validate_phone_number

"""
from datetime import datetime
from re import (
    match,
    sub
)


def validate_string(string: str) -> bool:

    result = True

    if not string:
        result = False

    elif len(string.strip()) == 0:
        result = False                      

    return result
    

def validate_cpf(string:str) -> bool:
    """
    Valida um CPF ou CNPJ
    
    - Args:
        - string:: str: String que será validada para ser, CPF ou CNPJ
        
    - Return:
        - str: CPF formatado (apenas números)
    
    - Raises:
        - HTTPException: Caso o tamanho da string seja inválido para ser um CPF ou CNPJ
    
    """

    identity = "".join([number for number in string if number.isnumeric()])

    result = False
    
    if len(identity) == 11: #Caso seja um CPF

        result = True


    return result


def validate_email(email:str) -> bool:
    """
    Valida um email
    
    - Args:
        - email:: str: Email que será validado
        
    - Return:
        - str: Email formatado
    
    - Raises:    
        - HTTPException: 400 - E-mail invalido
    
    """
    email = email.replace(" ", "").lower()
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    result = True

    if not match(email_regex, email):
        result = False
    
    return result

def validate_date(date:str) -> bool:
    """
    Valida uma data no formato YYYY-MM-DD
    
    - Args:
        - date:: str: Data que será validada
        
    - Return:
        - str: Data formatada
    
    - Raises:    
        - HTTPException: 400 - Data invalida
    
    """

    result = True
    
    if type(date) != str:
        return False

    # Definindo o formato esperado de data (YYYY-MM-DD)
    date_format = r'\d{4}-\d{2}-\d{2}'
    
    # Verificando se a data fornecida corresponde ao formato esperado
    if match(date_format, date):
        # Convertendo a data para um objeto datetime
        parsed_date = datetime.strptime(date, '%Y-%m-%d')
        # Verificando se a data de nascimento é no passado
        if parsed_date >= datetime.now():
            result =  False
        elif datetime.now().year - parsed_date.year < 18:
            result =  False
    else:
        result =  False
    
    return result
    
def validate_phone_number(phone_number: str) -> bool:
    """
    Remove todos os caracteres especiais de um número de telefone e valida o formato.
    
    - Args:
        - phone_number: str: Número de telefone que será limpo e validado
        
    - Return:
        - str: Número de telefone contendo apenas dígitos e no formato correto
    
    - Raises:    
        - HTTPException: 400 - Número de telefone inválido
    """

    if not isinstance(phone_number, str):
        return False
    
    result = True
    
    # Removendo todos os caracteres que não são dígitos
    cleaned_number = sub(r'\D', '', phone_number)
    
    # Definindo o formato esperado de número de telefone brasileiro com DDD e dígito 9
    phone_regex = r'^\d{2}9\d{8}$'
    
    # Verificando se o número de telefone limpo corresponde ao formato esperado
    if not match(phone_regex, cleaned_number):
        result = False
        # raise HTTPException(400, 'Número de telefone inválido. Deve conter 11 dígitos no formato correto (XX9XXXXXXXX)')
    
    return result