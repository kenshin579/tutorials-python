"""Flag, IntFlag - 비트 연산 Enum"""

from enum import Flag, IntFlag, auto


class Permission(Flag):
    READ = auto()     # 1
    WRITE = auto()    # 2
    EXECUTE = auto()  # 4

    # 조합 멤버
    READ_WRITE = READ | WRITE
    ALL = READ | WRITE | EXECUTE


class FilePermission(IntFlag):
    """UNIX 스타일 파일 퍼미션"""
    OWNER_READ = 0o400
    OWNER_WRITE = 0o200
    OWNER_EXEC = 0o100
    GROUP_READ = 0o040
    GROUP_WRITE = 0o020
    GROUP_EXEC = 0o010
    OTHER_READ = 0o004
    OTHER_WRITE = 0o002
    OTHER_EXEC = 0o001

    # 편의 조합
    OWNER_ALL = OWNER_READ | OWNER_WRITE | OWNER_EXEC  # 0o700
    DEFAULT = OWNER_ALL | GROUP_READ | GROUP_EXEC | OTHER_READ | OTHER_EXEC  # 0o755


def check_permission(perm: Permission, required: Permission) -> bool:
    """주어진 권한에 필요 권한이 포함되어 있는지 확인한다."""
    return required in perm


def combine_permissions(*perms: Permission) -> Permission:
    """여러 권한을 OR 조합한다."""
    result = Permission(0)
    for p in perms:
        result = result | p
    return result
