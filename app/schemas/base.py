from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    def dict(self, **kwargs) -> dict:
        result =  super().model_dump()
        result = {k: v for k, v in result.items() if v is not None}

        for k,v in kwargs.items():
            result[k] = v
        return result

