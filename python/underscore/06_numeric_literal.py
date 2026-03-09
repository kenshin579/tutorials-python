"""숫자 리터럴에서의 언더스코어 예제 (Python 3.6+)"""

# 10진수 - 자릿수 구분으로 가독성 향상
MILLION = 1_000_000
BILLION = 1_000_000_000
PRICE = 29_900

# 16진수
HEX_COLOR = 0xFF_FF_FF  # 흰색
HEX_MASK = 0xFF_00

# 2진수
BYTE_MASK = 0b1111_0000
PERMISSIONS = 0b0111_0101

# 8진수
OCTAL_PERM = 0o7_55

# 소수점
PI = 3.14_15_92
AVOGADRO = 6.022_140_76e23


def format_examples() -> dict:
    """다양한 숫자 리터럴 형식을 반환한다."""
    return {
        "million": MILLION,
        "billion": BILLION,
        "hex_color": HEX_COLOR,
        "hex_mask": HEX_MASK,
        "byte_mask": BYTE_MASK,
        "permissions": PERMISSIONS,
        "octal_perm": OCTAL_PERM,
        "pi": PI,
        "avogadro": AVOGADRO,
    }
