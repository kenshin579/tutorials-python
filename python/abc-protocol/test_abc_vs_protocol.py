"""ABC vs Protocol: 동일 인터페이스를 두 방식으로 구현하여 비교"""

import unittest
from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable


# ============================================================
# ABC 방식: 명시적 서브타이핑 (nominal subtyping)
# ============================================================
class NotifierABC(ABC):
    @abstractmethod
    def send(self, message: str) -> str:
        pass


class EmailNotifierABC(NotifierABC):
    """반드시 NotifierABC를 상속해야 함"""

    def send(self, message: str) -> str:
        return f"[Email] {message}"


class SlackNotifierABC(NotifierABC):
    def send(self, message: str) -> str:
        return f"[Slack] {message}"


# ============================================================
# Protocol 방식: 구조적 서브타이핑 (structural subtyping)
# ============================================================
@runtime_checkable
class NotifierProtocol(Protocol):
    def send(self, message: str) -> str: ...


class EmailNotifierProto:
    """상속 없이 send() 메서드만 구현하면 됨"""

    def send(self, message: str) -> str:
        return f"[Email] {message}"


class SlackNotifierProto:
    def send(self, message: str) -> str:
        return f"[Slack] {message}"


# 외부 라이브러리 클래스 (수정 불가)
class ThirdPartyNotifier:
    """서드파티 클래스: 우연히 send() 메서드가 있음"""

    def send(self, message: str) -> str:
        return f"[ThirdParty] {message}"


# ============================================================
# 사용 함수
# ============================================================
def notify_abc(notifier: NotifierABC, message: str) -> str:
    return notifier.send(message)


def notify_protocol(notifier: NotifierProtocol, message: str) -> str:
    return notifier.send(message)


class TestABCApproach(unittest.TestCase):
    def test_abc_notifiers(self):
        email = EmailNotifierABC()
        slack = SlackNotifierABC()
        assert notify_abc(email, "hello") == "[Email] hello"
        assert notify_abc(slack, "hello") == "[Slack] hello"

    def test_abc_isinstance(self):
        email = EmailNotifierABC()
        assert isinstance(email, NotifierABC)

    def test_abc_requires_inheritance(self):
        """ABC 방식: 상속 없이는 타입 검사 실패"""
        third_party = ThirdPartyNotifier()
        assert not isinstance(third_party, NotifierABC)

    def test_abc_enforces_implementation(self):
        """ABC 방식: 추상 메서드 미구현 시 TypeError"""

        class BadNotifier(NotifierABC):
            pass

        with self.assertRaises(TypeError):
            BadNotifier()


class TestProtocolApproach(unittest.TestCase):
    def test_protocol_notifiers(self):
        email = EmailNotifierProto()
        slack = SlackNotifierProto()
        assert notify_protocol(email, "hello") == "[Email] hello"
        assert notify_protocol(slack, "hello") == "[Slack] hello"

    def test_protocol_isinstance(self):
        email = EmailNotifierProto()
        assert isinstance(email, NotifierProtocol)

    def test_protocol_works_with_third_party(self):
        """Protocol 방식: 서드파티 클래스도 메서드만 맞으면 호환"""
        third_party = ThirdPartyNotifier()
        assert isinstance(third_party, NotifierProtocol)
        assert notify_protocol(third_party, "hello") == "[ThirdParty] hello"

    def test_protocol_no_runtime_enforcement(self):
        """Protocol 방식: 런타임에 구현 강제하지 않음 (타입 체커가 검사)"""

        class BadNotifier:
            pass

        # 인스턴스 생성은 가능 (TypeError 발생하지 않음)
        bad = BadNotifier()
        # 하지만 isinstance는 False
        assert not isinstance(bad, NotifierProtocol)


class TestComparisonSummary(unittest.TestCase):
    def test_abc_vs_protocol_key_differences(self):
        """
        ABC vs Protocol 핵심 차이:
        - ABC: 상속 필수, 런타임 강제, 강한 결합
        - Protocol: 상속 불필요, 타입 체커 검사, 느슨한 결합
        """
        # ABC: 서드파티 클래스 사용 불가 (상속 필수)
        assert not isinstance(ThirdPartyNotifier(), NotifierABC)

        # Protocol: 서드파티 클래스도 사용 가능
        assert isinstance(ThirdPartyNotifier(), NotifierProtocol)


if __name__ == "__main__":
    unittest.main()
