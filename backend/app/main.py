from fastapi import FastAPI

from app.providers.router import router as router_providers
from app.customers.router import router as router_customers


app = FastAPI()

app.include_router(router_providers)
app.include_router(router_customers)
