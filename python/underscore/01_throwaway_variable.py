"""변수로서의 언더스코어 (_) 예제"""


# 2.1 무시 변수 - for 루프에서 값이 필요 없을 때
def repeat_hello(n: int) -> list[str]:
    """n번 반복하여 'hello' 리스트를 반환한다."""
    return ["hello" for _ in range(n)]


# 2.2 무시 변수 - 튜플 언패킹에서 불필요한 값 무시
def get_first_and_last(data: tuple) -> tuple:
    """3개 요소 튜플에서 첫 번째와 마지막 값만 추출한다."""
    first, _, last = data
    return first, last


# 여러 값 무시 - 확장 언패킹
def get_first_item(data: tuple) -> object:
    """튜플에서 첫 번째 값만 추출한다."""
    first, *_ = data
    return first


def get_last_item(data: tuple) -> object:
    """튜플에서 마지막 값만 추출한다."""
    *_, last = data
    return last


# 2.3 국제화(i18n) 관례
def i18n_example() -> str:
    """gettext 함수를 _로 별칭하는 일반적인 패턴을 보여준다."""
    import gettext

    # 실제 프로젝트에서는 locale 설정과 함께 사용
    _ = gettext.gettext
    return _("Hello, World!")
