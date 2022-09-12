# FastAPI
from fastapi import FastAPI

# Tortoise
from tortoise.contrib.starlette import register_tortoise

# Config
from app.config import tortoise_config
# from app.config.static import add_static


def init(app: FastAPI):
    """
    Init routers and etc.
    :return:
    """
    init_routers(app)
    init_db(app)
    # add_static(app)


def init_db(app: FastAPI):
    """
    Init database models.
    :param app:
    :return:
    """
    register_tortoise(
        app,
        db_url=tortoise_config.db_url,
        generate_schemas=tortoise_config.generate_schemas,
        modules=tortoise_config.modules,
    )


def init_routers(app: FastAPI):
    """
    Initialize routers defined in `app.api`
    :param app:
    :return:
    """
    from app.core.routers import hello
    from app.core.routers import user_router
    from app.core.routers import message_router
    from app.core.routers import way_router

    app.include_router(router=hello.router, prefix="/hello", tags=["hello"])
    app.include_router(router=user_router.router,
                       prefix="/users",
                       tags=["users"])
    app.include_router(router=message_router.router,
                       prefix="/messages",
                       tags=["messages"])
    app.include_router(router=way_router.router,
                       prefix="/ways",
                       tags=["ways"])
