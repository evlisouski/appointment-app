

from app.users.models import User
from sqladmin import ModelView, Admin

from app.customers.models import Customer
from app.providers.models import Provider, Tag
from app.appointments.models import Appointment


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email]
    column_details_exclude_list = [User.hashed_password]
    can_delete = False
    name = "User"
    name_plural = "Users"
    # icon = "fa-solid fa-user"
    # category = "accounts"

class CustomerAdmin(ModelView, model=Customer):
    column_list = [c.name for c in Customer.__table__.c] + [Customer.users]
    column_details_exclude_list = [User.hashed_password]
    can_delete = True
    name = "Customer"
    name_plural = "Customers"
    # icon = "fa-solid fa-user"
    # category = "Roles"
    
class ProviderAdmin(ModelView, model=Provider):
    column_list = [c.name for c in Provider.__table__.c] + [Provider.users, Provider.tags]    
    can_delete = True
    name = "Provider"
    name_plural = "Providers"
    
class TagAdmin(ModelView, model=Tag):
    column_list = [c.name for c in Tag.__table__.c] + [Tag.providers]    
    can_delete = True
    name = "Tag"
    name_plural = "Tags"
    
class AppointmentAdmin(ModelView, model=Appointment):
    column_list = [c.name for c in Appointment.__table__.c] + [Appointment.customer_id, Appointment.providers]    
    can_delete = True
    name = "Appointment"
    name_plural = "Appointments"