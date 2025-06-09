import asyncio
from uuid import UUID, uuid4

import uvicorn
from fastapi import FastAPI, HTTPException

from examples.data.models import User, UserCreate
from examples.data.settings import get_mongo_settings
from src.core.storage.mongo_storage.storage import get_mongo_storage


def fastapi_example() -> None:
    app = FastAPI()
    settings = get_mongo_settings()

    @app.post("/users")
    async def add_user(user_create: UserCreate) -> User:
        storage = get_mongo_storage(settings)
        user = User(
            id=uuid4(),
            login=user_create.login,
            password=user_create.password,
        )
        return await storage.save(str(user.id), user)

    @app.get("/users/{user_id}")
    async def get_user(user_id: UUID) -> User:
        storage = get_mongo_storage(settings)
        user = await storage.load(str(user_id), User)
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        return user

    uvicorn.run(app)


async def main() -> None:
    settings = get_mongo_settings()
    storage = get_mongo_storage(settings)

    user_create = User(
        id=uuid4(),
        login="my_login",
        password="my_password",  # noqa
    )
    key = str(user_create.id)

    await storage.save(key, user_create)
    saved = await storage.load(key, User)
    print(saved.model_dump() if saved else None)  # noqa


if __name__ == "__main__":
    ex_num = int(input("enter num [0 - basic, 1 - fastapi]: ") or "0")
    match ex_num:
        case 0:
            asyncio.run(main())
        case 1:
            fastapi_example()
