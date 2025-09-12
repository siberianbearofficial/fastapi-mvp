# FastAPI MVP

FastAPI MVP helps you bootstrap a FastAPI application with minimal boilerplate. It provides ready-to-use MongoDB and S3 storage helpers, Prometheus metrics instrumentation, and strict environment management.

## Installation

```bash
pip install fastapi-mvp
```

## Quick start

Create an application that connects to MongoDB and exposes Prometheus metrics:

```python
from uuid import UUID
from fastapi import HTTPException
from pydantic import BaseModel

from fastapi_mvp import FastAPIMvp, MongoDep
from fastapi_mvp.metrics import MetricsSettings
from fastapi_mvp.storage.mongo_storage import MongoSettings

class User(BaseModel):
    id: UUID
    login: str
    password: str

app = FastAPIMvp(
    mongo=MongoSettings(
        name="mongo",
        user="mongo",
        password="mongo",
        host="localhost",
        port=27017,
    ),
    metrics=MetricsSettings(),
)

@app.get("/users/{user_id}")
async def get_user(user_id: UUID, mongo: MongoDep) -> User:
    user = await mongo.load(str(user_id), User)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user
```

Run the service with:

```python
import uvicorn

uvicorn.run(app)
```

`FastAPIMvp` is a singleton – attempting to create more than one instance raises `RuntimeError`.

## MongoDB storage

The library wraps a Motor client and lets you store Pydantic models without writing database boilerplate:

```python
from uuid import UUID, uuid4
from pydantic import BaseModel

from fastapi_mvp.storage.mongo_storage import MongoSettings, get_mongo_storage

class User(BaseModel):
    id: UUID
    login: str
    password: str

settings = MongoSettings(
    name="mongo",
    user="mongo",
    password="mongo",
    host="localhost",
    port=27017,
)
storage = get_mongo_storage(settings)

user = User(id=uuid4(), login="my_login", password="my_password")
key = str(user.id)
await storage.save(key, user)
saved = await storage.load(key, User)
```

In FastAPI routes, inject the storage via `MongoDep`:

```python
from uuid import UUID, uuid4
from fastapi import HTTPException
from pydantic import BaseModel
from fastapi_mvp import MongoDep

class UserCreate(BaseModel):
    login: str
    password: str

class User(BaseModel):
    id: UUID
    login: str
    password: str

@app.post("/users")
async def add_user(user_create: UserCreate, mongo: MongoDep) -> User:
    user = User(id=uuid4(), login=user_create.login, password=user_create.password)
    return await mongo.save(str(user.id), user)

@app.get("/users/{user_id}")
async def get_user(user_id: UUID, mongo: MongoDep) -> User:
    user = await mongo.load(str(user_id), User)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user
```

## S3 storage

`S3Storage` uses `aiobotocore` to store and retrieve binary data:

```python
from datetime import timedelta
from uuid import uuid4

from fastapi_mvp.storage.s3_storage import S3Settings, get_s3_storage

settings = S3Settings(
    bucket="test",
    host="localhost",
    protocol="http",
    region="ru-central-1",
    aws_access_key_id="test",
    aws_secret_access_key="test",
)
storage = get_s3_storage(settings)

data = b"hello world"
key = str(uuid4())
await storage.save(key, data, expires_in=timedelta(days=1))
saved = await storage.load(key)
```

Inside FastAPI handlers, inject the storage using `S3Dep`:

```python
from datetime import timedelta
from uuid import UUID, uuid4
from fastapi import Response, UploadFile
from fastapi_mvp import S3Dep

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
```

## Prometheus metrics

Provide `MetricsSettings` to expose request metrics on `/metrics`:

```python
from fastapi_mvp import FastAPIMvp
from fastapi_mvp.metrics import MetricsSettings

app = FastAPIMvp(
    metrics=MetricsSettings(excluded_handlers=["/healthz"]),
)
```

## Loading environment variables

Load values from `.env` files before creating the application:

```python
from pathlib import Path
from fastapi_mvp import FastAPIMvp
from fastapi_mvp.settings import LoadEnvSettings

FastAPIMvp.prepare_env(
    LoadEnvSettings(
        env="example",
        envs_dir=Path("examples/load_env_example"),
    )
)
```

`LoadEnvSettings` reads the specified `<env>.env` file and an optional `secrets.env` file in the same directory.

## Validating application settings

Inherit your configuration from `AppSettings` to ensure that all required variables are defined:

```python
from pydantic_settings import SettingsConfigDict
from fastapi_mvp.settings import AppSettings

class MyAppSettings(AppSettings):
    model_config = SettingsConfigDict(env_prefix="MY_APP__")
    something: int

FastAPIMvp()  # raises RuntimeError if MY_APP__SOMETHING is missing
```

`AppSettings.load_and_validate()` runs automatically during application startup and raises a clear error when variables are missing.

## Accessing storages globally

The library exposes helper functions that return the initialized storages from the singleton application:

```python
from fastapi_mvp import FastAPIMvp, get_mongo, get_s3

app = FastAPIMvp(...)

mongo_storage = get_mongo()
s3_storage = get_s3()
```

These helpers call `FastAPIMvp.instance()` internally and can be used outside request handlers.

