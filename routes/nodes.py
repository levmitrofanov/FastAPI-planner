from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from typing import List
from database.connection import get_session
from models.nodes import NetworkNode, NetworkNodeUpdate

node_router = APIRouter(
    tags=["Network Nodes"]
)

@node_router.post("/new")
async def create_node(new_node: NetworkNode, session=Depends(get_session)) -> dict:
    session.add(new_node)
    session.commit()
    session.refresh(new_node)
    return {
        "message": "Network node registered successfully",
        "id": new_node.id
    }

@node_router.get("/", response_model=List[NetworkNode])
async def retrieve_all_nodes(session=Depends(get_session)) -> List[NetworkNode]:
    statement = select(NetworkNode)
    nodes = session.exec(statement).all()
    return nodes

@node_router.get("/{id}", response_model=NetworkNode)
async def retrieve_node(id: int, session=Depends(get_session)) -> NetworkNode:
    node = session.get(NetworkNode, id)
    if node:
        return node
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Network node with supplied ID does not exist"
    )

@node_router.put("/edit/{id}", response_model=NetworkNode)
async def update_node(id: int, new_data: NetworkNodeUpdate, session=Depends(get_session)) -> NetworkNode:
    node = session.get(NetworkNode, id)
    if node:
        node_data = new_data.model_dump(exclude_unset=True) if hasattr(new_data, "model_dump") else new_data.dict(exclude_unset=True)
        for key, value in node_data.items():
            setattr(node, key, value)
        session.add(node)
        session.commit()
        session.refresh(node)
        return node
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Network node with supplied ID does not exist"
    )

@node_router.delete("/delete/{id}")
async def delete_node(id: int, session=Depends(get_session)) -> dict:
    node = session.get(NetworkNode, id)
    if node:
        session.delete(node)
        session.commit()
        return {
            "message": "Network node removed successfully"
        }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Network node with supplied ID does not exist"
    )
