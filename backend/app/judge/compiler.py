import subprocess
import time

from app.judge.models import (
    CompilationResult,
    ExecutionResult,
)


def compile_command(
    command: list[str],
    working_directory: str,
) -> CompilationResult:

    result = subprocess.run(
        command,
        cwd=working_directory,
        capture_output=True,
        text=True,
    )

    return CompilationResult(
        success=result.returncode == 0,
        compiler_output=result.stderr,
    )


def execute_command(
    command: list[str],
    stdin: str,
    working_directory: str,
    time_limit_ms: int,
) -> ExecutionResult:

    start = time.perf_counter()

    try:
        process = subprocess.run(
            command,
            input=stdin,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=time_limit_ms / 1000,
        )

        end = time.perf_counter()

        memory = 0

        return ExecutionResult(
            stdout=process.stdout,
            stderr=process.stderr,
            execution_time_ms=int(
                (end - start) * 1000
            ),
            memory_used_kb=memory,
            timed_out=False,
            exit_code=process.returncode,
        )

    except subprocess.TimeoutExpired:

        end = time.perf_counter()

        return ExecutionResult(
            stdout="",
            stderr="Execution timed out.",
            execution_time_ms=int(
                (end - start) * 1000
            ),
            memory_used_kb=0,
            timed_out=True,
            exit_code=-1,
        )