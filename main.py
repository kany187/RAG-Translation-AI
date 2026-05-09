from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.generate import router
from routes.agent import router as agent_router

app = FastAPI()

app.include_router(router)
app.include_router(agent_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}