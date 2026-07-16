from pathlib import Path

from app.judge.compiler import (
    compile_command,
    execute_command,
)
from app.judge.interfaces import BaseExecutor
from app.judge.models import (
    CompilationResult,
    ExecutionResult,
)


class CppExecutor(BaseExecutor):
    
    EXECUTABLE_NAME = "solution"

    def compile(
        self,
        source_file: str,
        working_directory: str,
    ) -> CompilationResult:

        return compile_command(
            command=[
                "g++",
                source_file,
                "-O2",
                "-std=c++17",
                "-o",
                self.EXECUTABLE_NAME,
            ],
            working_directory=working_directory,
        )

    def execute(
        self,
        executable_path: str,
        stdin: str,
        working_directory: str,
        time_limit_ms: int,
    ) -> ExecutionResult:

        executable = str(
            Path(working_directory) / self.EXECUTABLE_NAME
        )

        return execute_command(
            command=[executable],
            stdin=stdin,
            working_directory=working_directory,
            time_limit_ms=time_limit_ms,
        )