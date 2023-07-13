from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import endpoints
from app.database.database import engine
from app.database.schema import load_mappers, mapper_registry

mapper_registry.metadata.create_all(engine)
load_mappers()

app = FastAPI()

app.include_router(endpoints.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
