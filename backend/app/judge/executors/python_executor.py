from app.judge.compiler import (
    compile_command,
    execute_command,
)
from app.judge.interfaces import BaseExecutor
from app.judge.models import (
    CompilationResult,
    ExecutionResult,
)
import sys

class PythonExecutor(BaseExecutor):

    def compile(
        self,
        source_file: str,
        working_directory: str,
    ) -> CompilationResult:
        

        return CompilationResult(
            success=True,
            compiler_output="",
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
                sys.executable,
                executable_path,
            ],
            stdin=stdin,
            working_directory=working_directory,
            time_limit_ms=time_limit_ms,
        )