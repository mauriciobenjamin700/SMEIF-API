from datetime import datetime


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


def format_date(date: datetime) -> str:
    """
    Formata uma data

    - Args:
        - date:: datetime: Data que será formatada

    - Return:
        - str: Data formatada
    """
    return date.strftime("%d/%m/%Y")


def unformat_date(date: str) -> datetime:
    """
    Desformata uma data no formato dd/mm/yyyy para um objeto datetime

    - Args:
        - date:: str: Data que será desformatada

    - Return:
        - datetime: Data desformatada
    """
    return datetime.strptime(date, "%d/%m/%Y")


def format_string_date(date: str) -> str:
    """
    Formata uma string de data no formato YYYY-MM-DD para dd/mm/yyyy

    - Args:
        - date:: str: Data que será formatada

    - Return:
        - str: Data formatada
    """
    return format_date(datetime.strptime(date, "%Y-%m-%d"))