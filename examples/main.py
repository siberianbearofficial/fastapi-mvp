from uuid import UUID

import uvicorn
from fastapi import FastAPI, HTTPException

from examples.data.models import User
from examples.data.settings import get_metrics_settings, get_mongo_settings
from fastapi_mvp import Mvp, MvpDep


async def create_app() -> FastAPI:
    app = FastAPI()
    await Mvp.setup(
        app=app,
        mongo=get_mongo_settings(),
        metrics=get_metrics_settings(),
    )

    @app.get("/users/{user_id}")
    async def get_user(
        mvp: MvpDep,
        user_id: UUID,
    ) -> User:
        user = await mvp.mongo().load(str(user_id), User)
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        return user

    return app


def main() -> None:
    uvicorn.run(create_app)


if __name__ == "__main__":
    main()
