from fastapi import HTTPException
from sqlalchemy.orm import Session


from schemas.classes import (
    ClassRequest,
    ClassEventRequest,
    ClassStudentRequest,
    ClassResponse
)