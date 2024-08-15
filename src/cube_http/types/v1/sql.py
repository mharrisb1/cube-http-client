from pydantic import BaseModel, Field


class V1SqlResult(BaseModel):
    sql: str = Field(description="Formatted SQL query with parameters")


class V1SqlResponse(BaseModel):
    sql: V1SqlResult = Field(description="SQL response object")
