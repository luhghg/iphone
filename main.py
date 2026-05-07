from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.routers import auth_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router.router)




if __name__ == "__main__":
    uvicorn.run("main:app", reload = True)