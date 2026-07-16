from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess
from app.judge.factory import JudgeFactory
from app.judge.models import JudgeResult
from app.judge.models import (
    CompilationResult,
    ExecutionResult,
)
from app.repositories.problem_repository import ProblemRepository
from app.repositories.submission_repository import SubmissionRepository
from app.repositories.test_case_repository import TestCaseRepository

from app.models.submission import (
    SubmissionStatus,
    SubmissionVerdict,
)
from app.judge.comparator import OutputComparator

class JudgeService:

    def __init__(
        self,
        submission_repository: SubmissionRepository,
        problem_repository: ProblemRepository,
        test_case_repository: TestCaseRepository,
    ):
        self.submission_repository = submission_repository
        self.problem_repository = problem_repository
        self.test_case_repository = test_case_repository

    def _create_workspace(self) -> TemporaryDirectory:
       
        return TemporaryDirectory(
            prefix="judge_",
        )
    @staticmethod
    def _get_source_filename(
        language: str,
    ) -> str:

        filenames = {
            "python": "solution.py",
            "cpp": "solution.cpp",
            "java": "Main.java",
        }

        try:
            return filenames[
                language.strip().lower()
            ]
        except KeyError:
            raise ValueError(
                f"Unsupported language: {language}"
            )
        
    def _write_source_file(
        self,
        workspace: str,
        filename: str,
        source_code: str,
    ) -> Path:
        file_path = (
            Path(workspace)
            / filename
        )

        file_path.write_text(
            source_code,
            encoding="utf-8",
        )

        return file_path
    
    @staticmethod
    def _get_executor(
        language: str,
    ):

        return JudgeFactory.get_executor(
            language
        )

    @staticmethod
    def _compile(
        executor,
        source_file: Path,
        workspace: str,
    ) -> CompilationResult:

        return executor.compile(
            source_file=str(
                source_file.name
            ),
            working_directory=workspace,
        )

    @staticmethod
    def _execute(
        executor,
        executable_path: str,
        stdin: str,
        workspace: str,
        time_limit_ms: int,
    ) -> ExecutionResult:

        return executor.execute(
            executable_path=executable_path,
            stdin=stdin,
            working_directory=workspace,
            time_limit_ms=time_limit_ms,
        )
    def _update_submission(
        self,
        submission,
        *,
        status: SubmissionStatus,
        verdict: SubmissionVerdict | None,
        execution_time_ms: int = 0,
        memory_used_kb: int = 0,
        compiler_output: str = "",
    ):
        
        submission.status = status
        submission.verdict = verdict
        submission.execution_time_ms = execution_time_ms
        submission.memory_used_kb = memory_used_kb
        submission.compiler_output = compiler_output

        return self.submission_repository.update_submission(
            submission
        )
    def judge_submission(
    self,
    submission_id: int,
    ):
   
        submission = self.submission_repository.get_submission_by_id(
            submission_id
        )

        if submission is None:
            raise ValueError("Submission not found.")

        if submission.status != SubmissionStatus.PENDING:
            raise ValueError(
                "Only pending submissions can be judged."
            )

        problem = self.problem_repository.get_problem_by_id(
            submission.problem_id
        )

        if problem is None:
            raise ValueError("Problem not found.")

        hidden_test_cases = (
            self.test_case_repository.get_hidden_test_cases_by_problem(
                submission.problem_id
            )
        )

        if not hidden_test_cases:
            raise ValueError(
                "No hidden test cases found for this problem."
            )

        submission.status = SubmissionStatus.RUNNING
        submission.verdict = None

        self.submission_repository.update_submission(
            submission
        )

        workspace = self._create_workspace()
        workspace_path = workspace.name

        try:
            source_filename = self._get_source_filename(
                submission.language
            )

            source_file = self._write_source_file(
                workspace=workspace_path,
                filename=source_filename,
                source_code=submission.source_code,
            )

            executor = self._get_executor(
                submission.language
            )

            compilation_result = self._compile(
                executor=executor,
                source_file=source_file,
                workspace=workspace_path,
            )

            if not compilation_result.success:

                return self._update_submission(
                    submission,
                    status=SubmissionStatus.COMPLETED,
                    verdict=SubmissionVerdict.COMPILATION_ERROR,
                    execution_time_ms=0,
                    memory_used_kb=0,
                    compiler_output=compilation_result.compiler_output,
                )

            executable_path = str(source_file)

            total_execution_time = 0
            peak_memory_used = 0

            judge_result = None

            comparator = OutputComparator()

            for test_case in hidden_test_cases:

                execution_result = self._execute(
                    executor=executor,
                    executable_path=executable_path,
                    stdin=test_case.input,
                    workspace=workspace_path,
                    time_limit_ms=problem.time_limit_ms,
                )

                total_execution_time += (
                    execution_result.execution_time_ms
                )

                peak_memory_used = max(
                    peak_memory_used,
                    execution_result.memory_used_kb,
                )
                '''memory_limit_kb = problem.memory_limit_mb * 1024

                if execution_result.memory_used_kb > memory_limit_kb:
                    judge_result = JudgeResult(
                        verdict=SubmissionVerdict.MEMORY_LIMIT_EXCEEDED,
                        execution_time_ms=total_execution_time,
                        memory_used_kb=peak_memory_used,
                        passed=False,
                    )

                    break'''
                
                if execution_result.timed_out:

                    judge_result = JudgeResult(
                        verdict=SubmissionVerdict.TIME_LIMIT_EXCEEDED,
                        execution_time_ms=total_execution_time,
                        memory_used_kb=peak_memory_used,
                        passed=False,
                    )

                    break

                
                if execution_result.exit_code != 0:

                    judge_result = JudgeResult(
                        verdict=SubmissionVerdict.RUNTIME_ERROR,
                        execution_time_ms=total_execution_time,
                        memory_used_kb=peak_memory_used,
                        compiler_output=execution_result.stderr,
                        passed=False,
                    )

                    break


                is_correct = comparator.compare(
                    expected=test_case.expected_output,
                    actual=execution_result.stdout,
                )

                if not is_correct:

                    judge_result = JudgeResult(
                        verdict=SubmissionVerdict.WRONG_ANSWER,
                        execution_time_ms=total_execution_time,
                        memory_used_kb=peak_memory_used,
                        passed=False,
                    )

                    break
             
            if judge_result is None:

                judge_result = JudgeResult(
                    verdict=SubmissionVerdict.ACCEPTED,
                    execution_time_ms=total_execution_time,
                    memory_used_kb=peak_memory_used,
                    compiler_output="",
                    passed=True,
                )

            
            return self._update_submission(
                submission,
                status=SubmissionStatus.COMPLETED,
                verdict=judge_result.verdict,
                execution_time_ms=judge_result.execution_time_ms,
                memory_used_kb=judge_result.memory_used_kb,
                compiler_output=judge_result.compiler_output,
            )

        except (
            ValueError,
            subprocess.SubprocessError,
            subprocess.TimeoutExpired,
        ) as exc:

            self._update_submission(
                submission,
                status=SubmissionStatus.FAILED,
                verdict=SubmissionVerdict.INTERNAL_ERROR,
                execution_time_ms=0,
                memory_used_kb=0,
                compiler_output=str(exc),
            )

            raise

        finally:
            workspace.cleanup()
            


    
