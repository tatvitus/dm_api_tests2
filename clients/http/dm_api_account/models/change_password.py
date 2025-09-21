from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)


class ChangePassword(BaseModel):
    model_config = ConfigDict(extra="forbid")
    login: str = Field(..., description="Логин")
    token: str = Field(..., description="Токен для сброса пароля")
    old_password: str = Field(..., description="старый пароль", serialization_alias="oldPassword")
    new_password: str = Field(..., description="новый пароль", serialization_alias="newPassword")
