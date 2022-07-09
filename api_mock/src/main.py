import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import user, role, session, user_role

from core import config


app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url='/api/v1/openapi',
    openapi_url='/api/v1/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(user.router, prefix='/api/v1/users', tags=['User'])
app.include_router(user_role.router, prefix='/api/v1/users', tags=['User Role'])
app.include_router(session.router, prefix='/api/v1/auth', tags=['Session'])
app.include_router(role.router, prefix='/api/v1/roles', tags=['Role'])


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        reload=True
    )
