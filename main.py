from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from database.connection import conn
from routes.users import user_router
from routes.events import event_router
from routes.nodes import node_router
import uvicorn

app = FastAPI(
    title="Planner API (SQLModel)",
    description="API планировщика событий и управления сетевыми узлами с подключением к реляционной СУБД SQLite через SQLModel",
    version="2.0.0"
)

# Register routes
app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")
app.include_router(node_router, prefix="/node")

@app.on_event("startup")
def on_startup():
    conn()

@app.get("/")
async def home():
    return RedirectResponse(url="/event/")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
