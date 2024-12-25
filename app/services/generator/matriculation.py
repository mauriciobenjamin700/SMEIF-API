from datetime import datetime
from os.path import (
    abspath,
    dirname,
    join
)


FILE = "sequence.txt"
FILE_PATH = join(dirname(abspath(__file__)), FILE) 
MATRICULATION_LENGTH = 11


def matriculation_generate() -> str:
    """
    Gera uma matrícula aleatória.

    A matrícula é composta por Ano e número de sequência de tamanho 7

    Exemplo: 20240000001
    """
    # Gera 6 dígitos aleatórios

    try:
        with open(FILE_PATH, 'r') as f:
            last_sequence = f.read().strip()
            if len(last_sequence) > 0:
                last_sequence = last_sequence
            else:
                last_sequence = '0'

    except FileNotFoundError:

        last_sequence = '0'

        
    year = str(datetime.now().year)

    matriculation = year

    idx = int(last_sequence) + 1

    last_sequence = str(idx)

    while (len(matriculation) + len(last_sequence)) < MATRICULATION_LENGTH:

        last_sequence = f"0{last_sequence}"

    matriculation = f"{matriculation}{last_sequence}"


    with open(FILE_PATH, 'w') as f:
        f.write(str(idx))

    return matriculation