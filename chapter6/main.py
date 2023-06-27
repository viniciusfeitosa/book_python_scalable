from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import endpoints
from database import connect_to_database, close_database_connection

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


@app.on_event("startup")
async def startup_event():
    app.database = await connect_to_database()


@app.on_event("shutdown")
async def shutdown_event():
    await close_database_connection(app.database)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
