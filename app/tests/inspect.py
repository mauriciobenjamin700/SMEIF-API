from sqlalchemy.orm import Session


from database.models import (
    ChildModel,
    ClassModel,
    DisciplinesModel,
    NoteModel
)
from schemas.note import NoteResponse


################################ MODEL #####################

def inspect_notes_model(Note1: NoteModel, note2: NoteModel):
    assert Note1.id == note2.id
    assert Note1.child_cpf == note2.child_cpf
    assert Note1.discipline_id == note2.discipline_id
    assert Note1.class_id == note2.class_id
    assert Note1.aval_number == note2.aval_number
    assert Note1.semester == note2.semester


############################## Responses ###################
def inspect_note_response_model(
    db_session: Session,
    response: NoteResponse, 
    model: NoteModel
):

    discipline = db_session.query(DisciplinesModel).filter_by(id=model.discipline_id).first()

    class_ = db_session.query(ClassModel).filter_by(id=model.class_id).first()

    student = db_session.query(ChildModel).filter_by(cpf=model.child_cpf).first()



    assert isinstance(response, NoteResponse)
    assert response.id == model.id
    assert response.semester == model.semester
    assert response.aval_number == model.aval_number
    assert response.points == model.points
    assert response.discipline_id == model.discipline_id
    assert response.class_id == model.class_id
    assert response.child_cpf == model.child_cpf
    assert response.student_name == student.name
    assert response.discipline_name == discipline.name
    assert response.class_name == class_.name



