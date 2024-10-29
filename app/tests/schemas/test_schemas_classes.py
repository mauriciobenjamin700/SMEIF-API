from fastapi import HTTPException
from pytest import raises


from schemas.classes import (
    ClassRequest,
    ClassEventRequest,
    ClassStudentRequest,
    ClassResponse
)
from utils.format import unformat_cpf


def test_ClassRequest_success():
    data = {
        "name": "Matemática",
        "room": "Sala 01",
        "teacher_cpf": "123.456.789-00"
    }
    schema = ClassRequest(**data)
    assert schema.name == data["name"]
    assert schema.room == data["room"]
    assert schema.teacher_cpf == unformat_cpf(data["teacher_cpf"])