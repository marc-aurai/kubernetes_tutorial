import pydantic as _pydantic


class _CreatePrediction(_pydantic.BaseModel):
    question1: list[str]
    question2: list[str]
    # q1_words: list[int]
    # q2_words: list[int]

class Predictions(_pydantic.BaseModel):
    id: str
    predictions: str

    class Config:
        orm_mode = True
