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


class JavaExecutor(BaseExecutor):
  
    MAIN_CLASS = "Main"

    def compile(
        self,
        source_file: str,
        working_directory: str,
    ) -> CompilationResult:

        return compile_command(
            command=[
                "javac",
                source_file,
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

        return execute_command(
            command=[
                "java",
                self.MAIN_CLASS,
            ],
            stdin=stdin,
            working_directory=working_directory,
            time_limit_ms=time_limit_ms,
        )