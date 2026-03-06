"""frozen=True: 불변 데이터클래스, __hash__, replace()"""

from dataclasses import FrozenInstanceError, dataclass, replace


# 1. frozen=True — 불변 인스턴스
@dataclass(frozen=True)
class Point:
    x: float
    y: float


# 2. frozen + __hash__ → dict 키, set 요소 가능
@dataclass(frozen=True)
class Color:
    r: int
    g: int
    b: int

    @property
    def hex(self) -> str:
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"


# 3. replace() — 불변 객체 복사 + 일부 값 변경
@dataclass(frozen=True)
class Config:
    host: str = "localhost"
    port: int = 8080
    debug: bool = False


if __name__ == "__main__":
    # 불변 인스턴스
    print("=== frozen=True ===")
    p = Point(1.0, 2.0)
    print(f"point: {p}")
    try:
        p.x = 10.0  # type: ignore[misc]
    except FrozenInstanceError as e:
        print(f"FrozenInstanceError: {e}")

    # __hash__ — dict 키/set 요소
    print("\n=== __hash__ (dict 키, set) ===")
    red = Color(255, 0, 0)
    green = Color(0, 255, 0)
    blue = Color(0, 0, 255)

    color_names = {red: "Red", green: "Green", blue: "Blue"}
    print(f"color_names[red]: {color_names[red]}")

    unique_colors = {red, green, blue, Color(255, 0, 0)}
    print(f"unique_colors 개수: {len(unique_colors)}")  # 3

    print(f"red.hex: {red.hex}")

    # replace()
    print("\n=== replace() ===")
    default_config = Config()
    dev_config = replace(default_config, debug=True)
    prod_config = replace(default_config, host="0.0.0.0", port=443)
    print(f"default: {default_config}")
    print(f"dev:     {dev_config}")
    print(f"prod:    {prod_config}")
