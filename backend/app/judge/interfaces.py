from abc import ABC, abstractmethod

from app.judge.models import (
    CompilationResult,
    ExecutionResult,
)


class BaseExecutor(ABC):

    @abstractmethod
    def compile(
        self,
        source_file: str,
        working_directory: str,
    ) -> CompilationResult:
        
        raise NotImplementedError

    @abstractmethod
    def execute(
        self,
        executable_path: str,
        stdin: str,
        working_directory: str,
        time_limit_ms: int,
    ) -> ExecutionResult:
       
        raise NotImplementedError