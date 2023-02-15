import random

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from models import fibonacci

app = FastAPI()


@app.get("/fibonacci/")
async def core():
    random_num = random.randint(1, 10)
    return {
        'random_num': random_num,
        'fib_result': fibonacci(random_num),
    }

Instrumentator().instrument(app).expose(app)
