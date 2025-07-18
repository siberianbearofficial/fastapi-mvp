from typing import Optional, Protocol, Type


class IStorage(Protocol):
    async def save[T](self, key: str, data: T) -> T: ...
    async def load[T](self, key: str, model_type: Type[T]) -> Optional[T]: ...
