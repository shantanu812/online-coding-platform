from dataclasses import dataclass


@dataclass(slots=True)
class CompilationResult:
    success: bool
    compiler_output: str = ""


@dataclass(slots=True)
class ExecutionResult:
    stdout: str
    stderr: str

    execution_time_ms: int
    memory_used_kb: int

    timed_out: bool
    exit_code: int


from dataclasses import dataclass


@dataclass(slots=True)
class JudgeResult:

    verdict: str

    execution_time_ms: int

    memory_used_kb: int

    compiler_output: str = ""

    passed: bool = False