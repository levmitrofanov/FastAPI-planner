from sqlmodel import SQLModel, Field
from typing import Optional

class NetworkNode(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hostname: str
    ip_address: str
    node_type: str
    status: str

    class Config:
        schema_extra = {
            "example": {
                "hostname": "core-switch-01",
                "ip_address": "192.168.1.1",
                "node_type": "Switch",
                "status": "active"
            }
        }

class NetworkNodeUpdate(SQLModel):
    hostname: Optional[str] = None
    ip_address: Optional[str] = None
    node_type: Optional[str] = None
    status: Optional[str] = None
