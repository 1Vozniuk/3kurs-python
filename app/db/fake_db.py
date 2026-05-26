from typing import Dict, List, Optional

from app.schemas.user import UserCreate, UserOut, UserUpdate

_users: Dict[int, UserOut] = {}
_next_id = 1


def list_users() -> List[UserOut]:
    return list(_users.values())


def get_user(user_id: int) -> Optional[UserOut]:
    return _users.get(user_id)


def create_user(payload: UserCreate) -> UserOut:
    global _next_id
    user = UserOut(id=_next_id, **payload.model_dump())
    _users[_next_id] = user
    _next_id += 1
    return user


def update_user(user_id: int, payload: UserUpdate) -> Optional[UserOut]:
    existing = _users.get(user_id)
    if existing is None:
        return None

    updated_data = existing.model_dump()
    updated_data.update(payload.model_dump(exclude_unset=True))
    user = UserOut(**updated_data)
    _users[user_id] = user
    return user


def delete_user(user_id: int) -> Optional[UserOut]:
    return _users.pop(user_id, None)
