from pydantic import BaseModel, Field


class AuthScheme(BaseModel):

    access_token: str = Field(description="JWT access token")
    refresh_token: str = Field(description="JWT refresh token")
    token_type: str = Field(description="Type of authorization token")


class RefreshScheme(BaseModel):
    refresh_token: str = Field(description="JWT refresh token")
