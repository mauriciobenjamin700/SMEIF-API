from datetime import datetime
from datetime import time


def format_cpf(cpf:str) -> str:
    """
    Formata um CPF

    - Args:
        - cpf:: str: CPF que será formatado ex(12312312312)

    - Return:
        - str: CPF formatado ex(123.123.123-12)
    """
    
    cpf = "".join([number for number in cpf if number.isnumeric()])
    
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


def unformat_cpf(cpf:str):
    """
    Desformata um CPF

    - Args:
        - cpf:: str: CPF que será desformatado ex(123.123.123-12)

    - Return:
        - str: CPF desformatado ex(12312312312)
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
        - phone:: str: Número de telefone que será desformatado ex((89) 91212-1212)

    - Return
        - str: Número de telefone desformatado (89912121212)


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
        - str: Data formatada no formato dd/mm/yyyy
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


def format_time(time: time) -> str:
    """
    Formata um horário

    - Args:
        - time:: _Time: Horário que será formatado

    - Return:
        - str: Horário formatado no formato HH:MM
    """
    return time.strftime("%H:%M")


def unformat_time(time: str = "08:00") -> time:
    """
    Formata um horário

    - Args:
        - time:: str: Horário que será formatado

    - Return:
        - str: Horário formatado em um objeto time
    """
    return datetime.strptime(time, "%H:%M").time()


def format_string_date(date: str) -> str:
    """
    Formata uma string de data no formato YYYY-MM-DD para dd/mm/yyyy

    - Args:
        - date:: str: Data que será formatada

    - Return:
        - str: Data formatada
    """
    return format_date(datetime.strptime(date, "%Y-%m-%d"))