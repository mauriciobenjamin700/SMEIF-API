from constants.child import (
    MESSAGE_CHILD_ASSOCIATE_PARENT_SUCCESS,
    MESSAGE_CHILD_DELETE_PARENT_SUCCESS,
    MESSAGE_CHILD_DELETE_SUCCESS
)
from schemas.base import Kinship

from schemas.child import (
    StudentResponse
)


def test_routes_student_add(
    api,
    mock_StudentRequest
):
    
    request = mock_StudentRequest.dict()

    response = api.post("/student/add", json=request)

    student = StudentResponse(**response.json())

    assert response.status_code == 201
    assert student.name == request["name"]
    
    

def test_routes_student_get(
    api,
    mock_student_on_db
):
    
    student_cpf = mock_student_on_db.cpf
    
    response = api.get("/student/get", params={
        "student_cpf": student_cpf
    })
    
    student = StudentResponse(**response.json())
    
    assert response.status_code == 200
    assert student.name == mock_student_on_db.name
    

def test_routes_student_list(
    api,
    mock_student_on_db,
):
    
    response = api.get("/student/list")
    
    students = [StudentResponse(**item) for item in response.json()]
    
    assert response.status_code == 200
    assert len(students) == 1
    assert students[0].name == mock_student_on_db.name
    

def test_routes_student_update(
    api,
    mock_ChildRequest_update,
):
    
    request = mock_ChildRequest_update.dict()
    
    response = api.put("/student/update", json=request)
    print(response.json())

    assert response.status_code == 200
    
    

def test_routes_student_delete(
    api,
    mock_student_on_db
):
    
    response = api.delete("/student/delete", params={
        "student_cpf": mock_student_on_db.cpf
    })
    assert response.status_code == 200
    assert response.json()["detail"] == MESSAGE_CHILD_DELETE_SUCCESS
    
    
def test_routes_student_change_class(
    api,
    mock_student_on_db,
    mock_new_class_on_db
):
    student_cpf = mock_student_on_db.cpf
    to_class_id = mock_new_class_on_db.id
    is_transfer = True
    
    response = api.put("/student/change-class", params={
        "student_cpf": student_cpf,
        "to_class_id": to_class_id,
        "is_transfer": is_transfer
    })
    print(response.json())
    
    assert response.status_code == 200
    assert response.json()["name"] == mock_student_on_db.name
    

def test_routes_student_add_parent(
    api,
    mock_student_on_db,
    mock_new_parent_on_db
):
    
    response = api.put(
        "/student/add-parent",
        params={
            "student_cpf":mock_student_on_db.cpf,
            "kinship":Kinship.UNCLE.value,
            "parent_cpf":mock_new_parent_on_db.cpf
        }
    )
    assert response.json()["detail"] == MESSAGE_CHILD_ASSOCIATE_PARENT_SUCCESS
    assert response.status_code == 200
    

def test_routes_student_remove_parent(
    api,
    mock_student_on_db_with_max_parents,
    mock_parent_on_db
):
    
    student = mock_student_on_db_with_max_parents
    parent = mock_parent_on_db
    
    response = api.put(
        "/student/remove-parent",
        params={
            "student_cpf":student.cpf,
            "parent_cpf":parent.cpf
        }
    )
    
    
    assert response.status_code == 200
    assert response.json()["detail"] == MESSAGE_CHILD_DELETE_PARENT_SUCCESS