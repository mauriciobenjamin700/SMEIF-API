def format_cpf(cpf:str) -> str:
    """
    Formata um CPF

    - Args:
        - cpf:: str: CPF que será formatado

    - Return:
        - str: CPF formatado
    """
    
    cpf = "".join([number for number in cpf if number.isnumeric()])
    
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


def unformat_cpf(cpf:str):
    """
    Desformata um CPF

    - Args:
        - cpf:: str: CPF que será desformatado

    - Return:
        - str: CPF desformatado
    """
    
    return "".join([number for number in cpf if number.isnumeric()])



def format_phone(number: str) -> str:
    """
    Formata um número de telefone

    - Args:
        - number:: str: Número de telefone que será formatado

    - Return:
        - str: Número de telefone formatado
    """
    number = "".join([number for number in number if number.isnumeric()])
    return f"({number[:2]}) {number[2:7]}-{number[7:]}"

def unformat_phone(phone: str):

    """
    Desformata um número de telefone

    - Args:
        - phone:: str: Número de telefone que será desformatado

    - Return
        - str: Número de telefone desformatado (apenas números)


    """
    return "".join([number for number in phone if number.isnumeric()])


def clean_string_field(string: str) -> str:
    """
    Limpa uma string

    - Args:
        - string:: str: String que será limpa

    - Return:
        - str: String limpa
    """
    return string.strip() if string else ""