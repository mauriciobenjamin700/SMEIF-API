from datetime import datetime


from schemas.base import (
    BaseSchema,
    PresenceType
)


class PresenceRequest(BaseSchema):
    class_event_id: str
    child_cpf: str
    type: PresenceType
    start_class: datetime
    end_class: datetime
    


class PresenceDB(PresenceRequest):
    id: str
