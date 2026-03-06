"""__post_init__: 초기화 후 검증, InitVar, 파생 필드"""

from dataclasses import InitVar, dataclass, field


# 1. 검증 로직
@dataclass
class Temperature:
    celsius: float

    def __post_init__(self) -> None:
        if self.celsius < -273.15:
            raise ValueError(f"절대영도 미만: {self.celsius}°C")


# 2. 파생 필드 — 다른 필드 값에서 계산
@dataclass
class Rectangle:
    width: float
    height: float
    area: float = field(init=False)
    perimeter: float = field(init=False)

    def __post_init__(self) -> None:
        self.area = self.width * self.height
        self.perimeter = 2 * (self.width + self.height)


# 3. InitVar — init에서만 받고 필드로 저장하지 않는 매개변수
@dataclass
class User:
    name: str
    email: str
    email_domain: str = field(init=False)
    greeting: str = field(init=False)
    uppercase: InitVar[bool] = False

    def __post_init__(self, uppercase: bool) -> None:
        self.email_domain = self.email.split("@")[1]
        self.greeting = f"Hello, {self.name.upper() if uppercase else self.name}!"


# 4. 복합 예제 — 검증 + 파생 필드
@dataclass
class Product:
    name: str
    price: float
    quantity: int
    discount: float = 0.0
    total: float = field(init=False)

    def __post_init__(self) -> None:
        if self.price < 0:
            raise ValueError(f"가격은 0 이상이어야 합니다: {self.price}")
        if not 0 <= self.discount <= 1:
            raise ValueError(f"할인율은 0~1 사이여야 합니다: {self.discount}")
        self.total = self.price * self.quantity * (1 - self.discount)


if __name__ == "__main__":
    # 검증
    print("=== 검증 ===")
    t = Temperature(100.0)
    print(f"temperature: {t}")
    try:
        Temperature(-300.0)
    except ValueError as e:
        print(f"error: {e}")

    # 파생 필드
    print("\n=== 파생 필드 ===")
    rect = Rectangle(10.0, 5.0)
    print(f"rect: {rect}")
    print(f"area: {rect.area}, perimeter: {rect.perimeter}")

    # InitVar
    print("\n=== InitVar ===")
    u1 = User("Alice", "alice@example.com")
    u2 = User("Bob", "bob@test.org", uppercase=True)
    print(f"u1: {u1}")
    print(f"u2: {u2}")

    # 복합 예제
    print("\n=== 복합 예제 ===")
    product = Product("Laptop", 1000.0, 2, discount=0.1)
    print(f"product: {product}")
    print(f"total: {product.total}")
