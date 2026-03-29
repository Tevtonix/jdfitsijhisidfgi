from uuid import UUID
from app.models.users import User


class AccessUser:
    """Класс для удобной проверки прав доступа пользователя"""

    def __init__(self, user: User, scopes: list[str]):
        self.user = user
        self.scopes: set[str] = set(scopes)

    def can(self, resource: str, action: str, owner_id: UUID | None = None) -> bool:
        """
        Проверяет, имеет ли пользователь право на действие.
        Примеры:
        - can("items", "read")
        - can("items", "write", owner_id=item.user_id)
        """
        # Полные права (items:read:any, items:write:any и т.д.)
        if f"{resource}:{action}:any" in self.scopes:
            return True

        # Права только на свои объекты
        if owner_id is not None and owner_id == self.user.id:
            if f"{resource}:{action}:own" in self.scopes:
                return True

        return False