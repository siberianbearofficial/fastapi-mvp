from uuid import UUID

import uvicorn
from fastapi import FastAPI, HTTPException

import fastapi_mvp
from examples.data.models import User
from examples.data.settings import get_metrics_settings, get_mongo_settings


def create_app() -> FastAPI:
    app = FastAPI()
    fastapi_mvp.Mvp.setup(
        app=app,
        mongo=get_mongo_settings(),
        metrics=get_metrics_settings(),
    )

    @app.get("/users/{user_id}")
    async def get_user(
        mvp: fastapi_mvp.MvpDep,
        user_id: UUID,
    ) -> User:
        user = await mvp.mongo().load(str(user_id), User)
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        return user

    return app


def main() -> None:
    app = create_app()
    uvicorn.run(app)


if __name__ == "__main__":
    main()
