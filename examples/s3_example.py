import asyncio
from datetime import timedelta
from uuid import UUID, uuid4

import uvicorn
from fastapi import Response, UploadFile

from examples.data.settings import get_s3_settings
from fastapi_mvp import FastAPIMvp, S3Dep
from fastapi_mvp.storage.s3_storage import get_s3_storage


def fastapi_example() -> None:
    app = FastAPIMvp(s3=get_s3_settings())

    @app.post("/upload")
    async def upload_file(file: UploadFile, s3: S3Dep) -> str:
        file_id = uuid4()
        file_bytes = await file.read()
        await s3.save(str(file_id), file_bytes, expires_in=timedelta(days=1))
        return str(file_id)

    @app.get("/download/{file_id}")
    async def download_file(file_id: UUID, s3: S3Dep) -> Response:
        file_bytes = await s3.load(str(file_id))
        return Response(content=file_bytes, media_type="application/octet-stream")

    uvicorn.run(app)


async def main() -> None:
    settings = get_s3_settings()
    storage = get_s3_storage(settings)

    data = b"hello world"
    key = str(uuid4())

    await storage.save(key, data, expires_in=timedelta(days=1))
    saved = await storage.load(key)
    print(saved.decode())  # noqa


if __name__ == "__main__":
    ex_num = int(input("enter num [0 - basic, 1 - fastapi]: ") or "0")
    match ex_num:
        case 0:
            asyncio.run(main())
        case 1:
            fastapi_example()
