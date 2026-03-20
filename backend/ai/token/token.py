from pydantic import BaseModel, Field, model_validator


class Token(BaseModel):
    description: str = Field(default="Not Set")
    input_token: int = Field(default=0)
    output_token: int = Field(default=0)
    reasoning_token: int = Field(default=0)
    total_token: int = Field(default=0)

    @model_validator(mode='after')
    def _compute_total_token(self) -> "Token":
        self.total_token = self.input_token + self.output_token
        return self
