from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession

from app.access import AccessUser
from app.models.items import Item, ItemUpdate, ItemCreate
from app.models.users import User
from app.repositories import items as items_repo
from app.repositories import users as users_repo


async def get_items_with_count(
    session: AsyncSession,
    current_user: AccessUser,
    q: str | None,
    limit: int,
    offset: int,
) -> tuple[list[Item], int]:
    if current_user.can("items", "read"):
        user_id = None
    else:
        user_id = current_user.user.id
    return await items_repo.list_items_with_count(
        session=session,
        q=q,
        user_id=user_id,
        limit=limit,
        offset=offset
    )


async def get_item_for_read(
    session: AsyncSession,
    current_user: AccessUser,
    item_id: UUID
) -> Item | None:
    item = await items_repo.get_item(session=session, item_id=item_id)
    if item is None:
        return None
    if current_user.can("items", "read", owner_id=item.user_id):
        return item
    return None


async def get_item_for_write(
    session: AsyncSession,
    current_user: AccessUser,
    item_id: UUID
) -> Item | None:
    item = await items_repo.get_item(session=session, item_id=item_id)
    if item is None:
        return None
    if current_user.can("items", "write", owner_id=item.user_id):
        return item
    return None


async def patch_item(
    session: AsyncSession,
    item_db: Item,
    item_data: ItemUpdate
) -> Item:
    return await items_repo.patch_item(
        session=session,
        item_db=item_db,
        item_data=item_data,
        new_user=None
    )


async def delete_item(
    session: AsyncSession,
    item_db: Item
) -> None:
    await items_repo.delete_item(session=session, item=item_db)


async def change_item_owner(
    session: AsyncSession,
    current_user: AccessUser,
    item_id: UUID,
    new_owner_id: UUID
) -> Item | None:
    if not current_user.can("items", "write"):
        return None

    item = await items_repo.get_item(session=session, item_id=item_id)
    if item is None:
        return None

    new_owner = await users_repo.get_user(session=session, user_id=new_owner_id)
    if new_owner is None:
        return None

    return await items_repo.patch_item(
        session=session,
        item_db=item,
        item_data=ItemUpdate(),
        new_user=new_owner
    )


async def create_item(
    session: AsyncSession,
    current_user: AccessUser,
    item_data: ItemCreate
) -> Item:
    owner = await session.get(User, current_user.user.id)
    if not owner:
        raise ValueError("Owner not found")
    return await items_repo.create_item(
        session=session,
        user=owner,
        item_data=item_data
    )