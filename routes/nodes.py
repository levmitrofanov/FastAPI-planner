from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status
from database.connection import Database
from models.nodes import NetworkNode, NetworkNodeUpdate
from typing import List

node_router = APIRouter(
    tags=["Network Nodes"]
)

node_database = Database(NetworkNode)

@node_router.post("/new")
async def create_node(body: NetworkNode) -> dict:
    await node_database.save(body)
    return {
        "message": "Network node registered successfully",
        "id": str(body.id)
    }

@node_router.get("/", response_model=List[NetworkNode])
async def retrieve_all_nodes() -> List[NetworkNode]:
    nodes = await node_database.get_all()
    return nodes

@node_router.get("/{id}", response_model=NetworkNode)
async def retrieve_node(id: PydanticObjectId) -> NetworkNode:
    node = await node_database.get(id)
    if not node:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Network node with supplied ID does not exist"
        )
    return node

@node_router.put("/{id}", response_model=NetworkNode)
async def update_node(id: PydanticObjectId, body: NetworkNodeUpdate) -> NetworkNode:
    updated_node = await node_database.update(id, body)
    if not updated_node:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Network node with supplied ID does not exist"
        )
    return updated_node

@node_router.delete("/{id}")
async def delete_node(id: PydanticObjectId) -> dict:
    node = await node_database.delete(id)
    if not node:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Network node with supplied ID does not exist"
        )
    return {
        "message": "Network node removed successfully"
    }
