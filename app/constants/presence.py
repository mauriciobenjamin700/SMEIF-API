from schemas.base import PresenceType


ERROR_PRESENCE_REQUIRED_FIELD_CLASS_EVENT_ID = "ID da Aula é obrigatório"


ERROR_PRESENCE_INVALID_FIELD_TYPE = f"Tipo de presença inválido. Valores válidos: {PresenceType.P.value}, {PresenceType.F.value}"