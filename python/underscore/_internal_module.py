"""from module import * 동작을 보여주기 위한 내부 모듈"""

public_var = "I am public"
_private_var = "I am private"


def public_func() -> str:
    return "public function"


def _private_func() -> str:
    return "private function"
