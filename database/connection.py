from beanie import init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, List, Any
from pydantic import BaseModel

try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings

from models.users import User
from models.events import Event
from models.nodes import NetworkNode

class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None

    class Config:
        env_file = ".env"

    async def initialize_database(self):
        try:
            client = AsyncIOMotorClient(self.DATABASE_URL, serverSelectionTimeoutMS=1000)
            await client.server_info()
            await init_beanie(
                database=client.get_default_database(),
                document_models=[Event, User, NetworkNode]
            )
        except Exception:
            from mongomock_motor import AsyncMongoMockClient
            mock_client = AsyncMongoMockClient()
            mock_db = mock_client.get_database("planner")
            async def patched_lcn(*args, **kwargs):
                return []
            mock_db.list_collection_names = patched_lcn
            await init_beanie(
                database=mock_db,
                document_models=[Event, User, NetworkNode]
            )

class Database:
    def __init__(self, model):
        self.model = model

    async def save(self, document) -> None:
        await document.create()
        return

    async def get(self, id: PydanticObjectId) -> Any:
        doc = await self.model.get(id)
        if doc:
            return doc
        return False

    async def get_all(self) -> List[Any]:
        docs = await self.model.find_all().to_list()
        return docs

    async def update(self, id: PydanticObjectId, body: BaseModel) -> Any:
        doc_id = id
        des_body = body.model_dump() if hasattr(body, "model_dump") else body.dict()
        des_body = {k: v for k, v in des_body.items() if v is not None}
        update_query = {
            "$set": {
                field: value for field, value in des_body.items()
            }
        }
        doc = await self.get(doc_id)
        if not doc:
            return False
        await doc.update(update_query)
        return doc

    async def delete(self, id: PydanticObjectId) -> bool:
        doc = await self.get(id)
        if not doc:
            return False
        await doc.delete()
        return True
