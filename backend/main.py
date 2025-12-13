from fastapi import FastAPI
from routes import profile_routes, item_routes

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(profile_routes.router)
app.include_router(item_routes.router)
