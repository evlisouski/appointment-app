import time
from uu import decode
from black import Encoding
from fastapi import FastAPI, Request
from fastapi_versioning import VersionedFastAPI
from prometheus_fastapi_instrumentator import Instrumentator
import sentry_sdk
from sqladmin import Admin

from app.logger import logger

from app.providers.router import router as router_providers
from app.customers.router import router as router_customers
from app.appointments.router import router as router_appointments
from app.users.router import router_users
from app.users.router import router_auth
from app.users.models import User
from app.database import engine
from app.admin.views import CustomerAdmin, UserAdmin, ProviderAdmin, TagAdmin, AppointmentAdmin
from app.admin.auth import authentication_backend
from app.prometheus.router import router as router_prometeus


from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis



sentry_sdk.init(
    dsn="http://cf536af1015243ca8133021d5bee3606@127.0.0.1:9000/4"
    # enable_tracing=True,
)

app = FastAPI()


app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router_providers)
app.include_router(router_customers)
app.include_router(router_appointments)

# Подключение версионирования
# app = VersionedFastAPI(app,
#                        version_format='{major}',
#                        prefix_format='/api/v{major}',
#                        )

admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UserAdmin)
admin.add_view(CustomerAdmin)
admin.add_view(ProviderAdmin)
admin.add_view(TagAdmin)
admin.add_view(AppointmentAdmin)
app.include_router(router_prometeus)

instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"],
    )
instrumentator.instrument(app).expose(app)

@app.on_event("startup")
async def startup():    
  
    redis = aioredis.from_url("redis://localhost:6379", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")




@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    # При подключении Prometheus + Grafana подобный лог не требуется
    logger.info("Request handling time", extra={
        "process_time": round(process_time, 4)
    })
    return response


