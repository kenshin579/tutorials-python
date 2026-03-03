from myapp.config import APP_NAME, DEBUG


def greet(name: str) -> str:
    return f"Hello, {name}! Welcome to {APP_NAME}."


def main() -> None:
    print(greet("World"))
    if DEBUG:
        print("Debug mode is ON")


if __name__ == "__main__":
    main()
