from typing import Optional, List
from beanie import Document
from pydantic import BaseModel

class NetworkNode(Document):
    hostname: str
    ip_address: str
    node_type: str
    status: str
    location: str
    tags: List[str] = []

    class Settings:
        name = "nodes"

    class Config:
        schema_extra = {
            "example": {
                "hostname": "core-switch-01",
                "ip_address": "192.168.1.1",
                "node_type": "Switch",
                "status": "active",
                "location": "Server Room A",
                "tags": ["core", "cisco", "datacenter"]
            }
        }

class NetworkNodeUpdate(BaseModel):
    hostname: Optional[str] = None
    ip_address: Optional[str] = None
    node_type: Optional[str] = None
    status: Optional[str] = None
    location: Optional[str] = None
    tags: Optional[List[str]] = None

    class Config:
        schema_extra = {
            "example": {
                "hostname": "core-switch-01",
                "status": "maintenance"
            }
        }
