from fastapi import Depends, FastAPI
from starlette.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Service appointment",
    version="0.1.0",
    root_path="/api",
)


origins = [
    # 3000 - React.js
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin",
                   "Authorization"],
)
