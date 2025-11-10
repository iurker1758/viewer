import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from viewer.auth.router import router as auth_router
from viewer.database.router import router as database_router
from viewer.public.utils import get_config

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(database_router)

if __name__ == "__main__":
    port_number = int(get_config("DEFAULT", "PORT"))
    uvicorn.run("main:app", host="0.0.0.0", port=port_number, reload=True)  # noqa: S104
