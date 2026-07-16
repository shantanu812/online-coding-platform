from app.judge.executors.cpp_executor import CppExecutor
from app.judge.executors.java_executor import JavaExecutor
from app.judge.executors.python_executor import PythonExecutor
from app.judge.interfaces import BaseExecutor


class JudgeFactory:
    
    _executors = {
        "python": PythonExecutor,
        "cpp": CppExecutor,
        "java": JavaExecutor,
    }

    @classmethod
    def get_executor(
        cls,
        language: str,
    ) -> BaseExecutor:
        executor = cls._executors.get(
            language.strip().lower()
        )

        if executor is None:
            raise ValueError(
                f"Unsupported language: {language}"
            )

        return executor()