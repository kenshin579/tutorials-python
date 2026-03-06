"""Generator 양방향 통신: send(), throw(), close()"""


# 1. send() - Generator에 값 전달
def running_average():
    """send()를 활용한 러닝 평균 계산기"""
    total = 0.0
    count = 0
    average = None

    while True:
        value = yield average
        if value is None:
            break
        total += value
        count += 1
        average = total / count


def echo():
    """send()로 받은 값을 그대로 yield하는 간단한 예제"""
    received = yield "ready"
    while True:
        received = yield f"echo: {received}"


# 2. throw() - Generator 내부에 예외 주입
def resilient_generator():
    """throw()로 예외를 주입받아 처리하는 Generator"""
    while True:
        try:
            value = yield
            print(f"  받은 값: {value}")
        except ValueError as e:
            print(f"  ValueError 처리: {e}")
        except GeneratorExit:
            print("  GeneratorExit → 정리 작업 수행")
            return


# 3. close() - Generator 종료
def resource_generator():
    """close() 시 리소스 정리 패턴"""
    print("  리소스 열기")
    try:
        while True:
            yield "data"
    except GeneratorExit:
        print("  리소스 닫기 (정리 완료)")


if __name__ == "__main__":
    # send() 예제
    print("=== 러닝 평균 계산기 (send) ===")
    avg = running_average()
    next(avg)  # Generator 초기화 (첫 yield까지 실행)
    print(f"send(10) → 평균: {avg.send(10)}")
    print(f"send(20) → 평균: {avg.send(20)}")
    print(f"send(30) → 평균: {avg.send(30)}")

    # echo 예제
    print("\n=== echo (send) ===")
    e = echo()
    print(f"next() → {next(e)}")
    print(f"send('hello') → {e.send('hello')}")
    print(f"send('world') → {e.send('world')}")

    # throw() 예제
    print("\n=== throw() 예외 주입 ===")
    gen = resilient_generator()
    next(gen)  # 초기화
    gen.send(42)
    gen.throw(ValueError, "잘못된 값")
    gen.send(100)
    gen.close()

    # close() 예제
    print("\n=== close() 리소스 정리 ===")
    res = resource_generator()
    print(f"next() → {next(res)}")
    res.close()
