from pydantic_settings import SettingsConfigDict

from fastapi_mvp import FastAPIMvp
from fastapi_mvp.settings import AppSettings


class MyAppSettings(AppSettings):
    model_config = SettingsConfigDict(env_prefix="MY_APP__")
    something: int


async def main() -> None:
    try:
        FastAPIMvp()
    except RuntimeError as e:
        msg = (
            "If you had set the 'something' field value, "
            f"the exception would not have raised: {e}"
        )
        print(msg)  # noqa


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
