from fastapi import FastAPI

from app.providers.router import router as router_providers
from app.customers.router import router as router_customers
from app.appointments.router import router as router_appointments
from app.users.router import router_users
from app.users.router import router_auth


app = FastAPI()

app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router_providers)
app.include_router(router_customers)
app.include_router(router_appointments)
