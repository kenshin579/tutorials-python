"""
실전 예제: 파일 비동기 처리
- aiofiles로 대량 파일 읽기/쓰기
- asyncio만으로 파일 I/O 처리 (loop.run_in_executor)
"""

import asyncio
import os
import tempfile
import time


# ============================================================
# 1. aiofiles 사용법
# ============================================================
async def aiofiles_example():
    """aiofiles로 비동기 파일 읽기/쓰기."""
    try:
        import aiofiles
    except ImportError:
        print("  aiofiles가 설치되지 않았습니다: pip install aiofiles")
        return None

    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, "test.txt")

    # 비동기 파일 쓰기
    async with aiofiles.open(file_path, mode="w", encoding="utf-8") as f:
        await f.write("Hello, asyncio!\n")
        await f.write("비동기 파일 I/O 테스트\n")
    print(f"  파일 쓰기 완료: {file_path}")

    # 비동기 파일 읽기
    async with aiofiles.open(file_path, mode="r", encoding="utf-8") as f:
        content = await f.read()
    print(f"  파일 내용: {content.strip()}")

    # 정리
    os.remove(file_path)
    os.rmdir(temp_dir)
    return content


# ============================================================
# 2. run_in_executor로 동기 파일 I/O 비동기 처리
# ============================================================
async def executor_file_io():
    """loop.run_in_executor로 동기 파일 I/O를 비동기로 처리한다."""
    temp_dir = tempfile.mkdtemp()
    loop = asyncio.get_running_loop()

    def write_file_sync(path: str, content: str):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    def read_file_sync(path: str) -> str:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    file_path = os.path.join(temp_dir, "executor_test.txt")

    # executor에서 동기 함수 실행
    await loop.run_in_executor(None, write_file_sync, file_path, "executor로 작성")
    content = await loop.run_in_executor(None, read_file_sync, file_path)
    print(f"  executor 파일 내용: {content}")

    os.remove(file_path)
    os.rmdir(temp_dir)
    return content


# ============================================================
# 3. 대량 파일 비동기 처리
# ============================================================
async def bulk_file_processing():
    """여러 파일을 동시에 비동기 처리한다."""
    temp_dir = tempfile.mkdtemp()
    num_files = 20
    sem = asyncio.Semaphore(5)  # 동시 파일 I/O 제한
    loop = asyncio.get_running_loop()

    # 파일 생성
    async def create_file(index: int):
        async with sem:
            path = os.path.join(temp_dir, f"file_{index:03d}.txt")
            content = f"파일 {index}의 내용\n" * 100

            def _write():
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)

            await loop.run_in_executor(None, _write)
            return path

    # 파일 읽기 + 처리
    async def process_file(path: str):
        async with sem:
            def _read():
                with open(path, "r", encoding="utf-8") as f:
                    return f.read()

            content = await loop.run_in_executor(None, _read)
            line_count = content.count("\n")
            return {"path": os.path.basename(path), "lines": line_count}

    # 파일 생성
    start = time.monotonic()
    paths = await asyncio.gather(*[create_file(i) for i in range(num_files)])
    create_time = time.monotonic() - start
    print(f"  {num_files}개 파일 생성: {create_time:.3f}s")

    # 파일 처리
    start = time.monotonic()
    results = await asyncio.gather(*[process_file(p) for p in paths])
    process_time = time.monotonic() - start
    print(f"  {num_files}개 파일 처리: {process_time:.3f}s")

    total_lines = sum(r["lines"] for r in results)
    print(f"  총 줄 수: {total_lines}")

    # 정리
    for p in paths:
        os.remove(p)
    os.rmdir(temp_dir)

    return results


# ============================================================
# 4. 파일 감시 (polling 방식)
# ============================================================
async def file_watcher_example():
    """파일 변경을 감시하는 간단한 비동기 패턴."""
    temp_dir = tempfile.mkdtemp()
    watch_file = os.path.join(temp_dir, "watched.txt")
    changes_detected = []

    # 초기 파일 생성
    with open(watch_file, "w") as f:
        f.write("initial")

    last_mtime = os.path.getmtime(watch_file)

    async def watcher():
        nonlocal last_mtime
        for _ in range(5):  # 5번만 체크
            await asyncio.sleep(0.1)
            try:
                mtime = os.path.getmtime(watch_file)
                if mtime != last_mtime:
                    last_mtime = mtime
                    with open(watch_file, "r") as f:
                        content = f.read()
                    changes_detected.append(content)
                    print(f"  변경 감지: {content}")
            except FileNotFoundError:
                break

    async def modifier():
        await asyncio.sleep(0.15)
        with open(watch_file, "w") as f:
            f.write("modified-1")
        await asyncio.sleep(0.2)
        with open(watch_file, "w") as f:
            f.write("modified-2")

    await asyncio.gather(watcher(), modifier())

    # 정리
    os.remove(watch_file)
    os.rmdir(temp_dir)

    print(f"  감지된 변경: {changes_detected}")
    return changes_detected


if __name__ == "__main__":
    print("=== 1. aiofiles 사용법 ===")
    asyncio.run(aiofiles_example())

    print("\n=== 2. run_in_executor ===")
    asyncio.run(executor_file_io())

    print("\n=== 3. 대량 파일 처리 ===")
    asyncio.run(bulk_file_processing())

    print("\n=== 4. 파일 감시 ===")
    asyncio.run(file_watcher_example())
