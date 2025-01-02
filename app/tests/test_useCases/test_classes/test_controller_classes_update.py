from useCases.classes import ClassesUseCases


def test_uc_classes_update_success(db_session, mock_class_on_db, mock_ClassRequest_update):

    uc = ClassesUseCases(db_session)

    request = mock_ClassRequest_update

    response = uc.update(mock_class_on_db.id, request)

    assert response.id == mock_class_on_db.id
    assert response.education_level == request.education_level
    assert response.name == request.name
    assert response.section == request.section
    assert response.shift == request.shift
    assert response.max_students == request.max_students
    assert response.class_info == uc.build_class_info(mock_class_on_db)
    assert response.class_events == []