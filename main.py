from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from database.connection import Settings
from routes.users import user_router
from routes.events import event_router
from routes.nodes import node_router
import uvicorn

settings = Settings()

app = FastAPI(
    title="Planner API (Beanie & MongoDB)",
    description="API планировщика событий и сетевых узлов с нереляционной базой данных MongoDB (ODM Beanie)",
    version="3.0.0"
)

app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")
app.include_router(node_router, prefix="/node")

@app.on_event("startup")
async def on_startup():
    await settings.initialize_database()

@app.get("/")
async def home():
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
