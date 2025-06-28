from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from fastapi_mvp import FastAPIMvp
from fastapi_mvp.settings import LoadEnvSettings


class InterestingSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="INTERESTING_SETTINGS__")

    first: int
    second: str


def main() -> None:
    FastAPIMvp.prepare_env(
        LoadEnvSettings(
            env="example",
            envs_dir=Path(__file__).parent,
        ),
    )

    settings = InterestingSettings()
    print(settings.first)  # noqa
    print(settings.second)  # noqa


if __name__ == "__main__":
    main()
