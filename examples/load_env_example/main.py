from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from fastapi_mvp import Mvp


class InterestingSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="INTERESTING_SETTINGS__")

    first: int
    second: str


async def main() -> None:
    await Mvp.load_env("example", envs_dir=Path(__file__).parent)

    settings = InterestingSettings()
    print(settings.first)  # noqa
    print(settings.second)  # noqa


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
