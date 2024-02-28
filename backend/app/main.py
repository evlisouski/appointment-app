from fastapi import FastAPI
from sqladmin import Admin

from app.providers.router import router as router_providers
from app.customers.router import router as router_customers
from app.appointments.router import router as router_appointments
from app.users.router import router_users
from app.users.router import router_auth
from app.users.models import User
from app.database import engine
from app.admin.views import CustomerAdmin, UserAdmin, ProviderAdmin, TagAdmin, AppointmentAdmin
from app.admin.auth import authentication_backend


app = FastAPI()

app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router_providers)
app.include_router(router_customers)
app.include_router(router_appointments)


admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UserAdmin)
admin.add_view(CustomerAdmin)
admin.add_view(ProviderAdmin)
admin.add_view(TagAdmin)
admin.add_view(AppointmentAdmin)