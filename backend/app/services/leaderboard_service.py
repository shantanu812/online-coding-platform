from collections import defaultdict
from datetime import datetime, timezone

from app.models.contest import Contest
from app.models.submission import SubmissionVerdict
from app.repositories.leaderboard_repository import LeaderboardRepository
from app.schemas.leaderboard import (
    LeaderboardEntry,
    LeaderboardResponse,
    ProblemScore,
)


class LeaderboardService:
    def __init__(
        self,
        repository: LeaderboardRepository,
    ):
        self.repository = repository

    def generate_leaderboard(
        self,
        contest_id: int,
    ) -> LeaderboardResponse:
        contest = self._get_contest(contest_id)
        
        self._validate_contest_started(contest)

        participants = (
            self.repository.get_contest_participants(
                contest_id
            )
        )
        problems = (
            self.repository.get_contest_problems(
                contest_id
            )
        )
        
        submissions = (
            self.repository.get_contest_submissions(
                contest_id
            )
        )
        
        submissions_by_user = (
            self.repository.get_submissions_grouped_by_user(
                contest_id
            )
        )
        submissions_by_problem = (
            self.repository.get_submissions_grouped_by_problem(
                contest_id
            )
        )
        accepted_submissions = (
            self.repository.get_accepted_submissions(
                contest_id
            )
        )
        wrong_submissions = (
            self.repository.get_wrong_submissions(
                contest_id
            )
        )
        
        scoreboard = self._initialize_scoreboard(
            participants
        )
        problem_scores = (
            self._initialize_problem_scores(
                participants=participants,
                problems=problems,
            )
        )
        
        leaderboard_context = {
            "contest": contest,
            "participants": participants,
            "problems": problems,
            "submissions": submissions,
            "submissions_by_user": submissions_by_user,
            "submissions_by_problem": submissions_by_problem,
            "accepted_submissions": accepted_submissions,
            "wrong_submissions": wrong_submissions,
            "scoreboard": scoreboard,
            "problem_scores": problem_scores,
        }

        leaderboard_entries = []

        for participant in participants:
            user_id = participant.id
            user_submissions = submissions_by_user.get(
                user_id,
                [],
            )
            scoreboard[user_id]["statistics"][
                "total_submissions"
            ] = len(user_submissions)
            
            for problem in problems:
                problem_score = problem_scores[user_id][
                    problem.id
                ]
                problem_submissions = [
                    submission
                    for submission in user_submissions
                    if submission.problem_id == problem.id
                ]
                if not problem_submissions:
                    scoreboard[user_id][
                        "problem_scores"
                    ][problem.id] = problem_score
                    continue
                    
                accepted_submission = None
                for submission in problem_submissions:
                    if (
                        submission.verdict
                        == SubmissionVerdict.ACCEPTED
                    ):
                        accepted_submission = submission
                        break
                        
                if accepted_submission is None:
                    wrong_attempts = len(
                        problem_submissions
                    )
                    problem_score.wrong_attempts = (
                        wrong_attempts
                    )
                    scoreboard[user_id][
                        "statistics"
                    ]["wrong_submissions"] += (
                        wrong_attempts
                    )
                    for submission in problem_submissions:
                        if (
                            submission.verdict
                            == SubmissionVerdict.COMPILATION_ERROR
                        ):
                            scoreboard[user_id][
                                "statistics"
                            ][
                                "compilation_errors"
                            ] += 1
                        elif (
                            submission.verdict
                            == SubmissionVerdict.RUNTIME_ERROR
                        ):
                            scoreboard[user_id][
                                "statistics"
                            ][
                                "runtime_errors"
                            ] += 1
                        elif (
                            submission.verdict
                            == SubmissionVerdict.TIME_LIMIT_EXCEEDED
                        ):
                            scoreboard[user_id][
                                "statistics"
                            ][
                                "time_limit_exceeded"
                            ] += 1
                        elif (
                            submission.verdict
                            == SubmissionVerdict.MEMORY_LIMIT_EXCEEDED
                        ):
                            scoreboard[user_id][
                                "statistics"
                            ][
                                "memory_limit_exceeded"
                            ] += 1
                    scoreboard[user_id][
                        "problem_scores"
                    ][problem.id] = problem_score
                    continue
                    
                
                wrong_before_accept = 0
                for submission in problem_submissions:
                    if submission.id == accepted_submission.id:
                        break
                    wrong_before_accept += 1
                    scoreboard[user_id][
                        "statistics"
                    ]["wrong_submissions"] += 1
                    if (
                        submission.verdict
                        == SubmissionVerdict.COMPILATION_ERROR
                    ):
                        scoreboard[user_id][
                            "statistics"
                        ][
                            "compilation_errors"
                        ] += 1
                    elif (
                        submission.verdict
                        == SubmissionVerdict.RUNTIME_ERROR
                    ):
                        scoreboard[user_id][
                            "statistics"
                        ][
                            "runtime_errors"
                        ] += 1
                    elif (
                        submission.verdict
                        == SubmissionVerdict.TIME_LIMIT_EXCEEDED
                    ):
                        scoreboard[user_id][
                            "statistics"
                        ][
                            "time_limit_exceeded"
                        ] += 1
                    elif (
                        submission.verdict
                        == SubmissionVerdict.MEMORY_LIMIT_EXCEEDED
                    ):
                        scoreboard[user_id][
                            "statistics"
                        ][
                            "memory_limit_exceeded"
                        ] += 1
                        
                scoreboard[user_id]["statistics"][
                    "accepted_submissions"
                ] += 1
                
                contest_minutes = int(
                    (
                        accepted_submission.created_at
                        - contest.start_time
                    ).total_seconds()
                    // 60
                )
                penalty = (
                    contest_minutes
                    + wrong_before_accept * 20
                )
                problem_score.solved = True
                problem_score.score = 1
                problem_score.penalty_minutes = penalty
                problem_score.wrong_attempts = (
                    wrong_before_accept
                )
                problem_score.accepted_submission_id = (
                    accepted_submission.id
                )
                problem_score.accepted_at_minutes = (
                    contest_minutes
                )
                scoreboard[user_id][
                    "problem_scores"
                ][problem.id] = problem_score
                
                scoreboard[user_id]["total_score"] += (
                    problem_score.score
                )
                
                if problem_score.solved:
                    scoreboard[user_id][
                        "solved_problems"
                    ] += 1
                    scoreboard[user_id][
                        "total_penalty"
                    ] += problem_score.penalty_minutes
                    
                    last_time = scoreboard[user_id][
                        "last_accepted_time"
                    ]
                    if (
                        last_time is None
                        or problem_score.accepted_at_minutes
                        > last_time
                    ):
                        scoreboard[user_id][
                            "last_accepted_time"
                        ] = (
                            problem_score.accepted_at_minutes
                        )
                        
        
            scoreboard[user_id]["problem_scores"] = [
                scoreboard[user_id]["problem_scores"][
                    problem.id
                ]
                for problem in problems
            ]

        
        unsorted_entries = list(scoreboard.values())

        unsorted_entries.sort(
            key=lambda x: (
                -x["solved_problems"],
                x["total_penalty"],
                x["last_accepted_time"] or 0,
            )
        )

        
        for rank, data in enumerate(
            unsorted_entries, 
            start=1,
        ):
            user = data["user"]
            entry = LeaderboardEntry(
                rank=rank,
                user_id=user.id,
                full_name=user.full_name,
                total_score=data["total_score"],
                solved_problems=data["solved_problems"],
                total_penalty=data["total_penalty"],
                last_accepted_time=data["last_accepted_time"],
                problem_scores=data["problem_scores"],
                statistics=data["statistics"],
            )
            leaderboard_entries.append(entry)

        return LeaderboardResponse(
            contest_id=contest.id,
            contest_title=contest.title,
            participant_count=len(participants),
            leaderboard=leaderboard_entries,
        )

    def _get_contest(
        self,
        contest_id: int,
    ) -> Contest:
        contest = self.repository.get_contest_by_id(
            contest_id
        )
        if contest is None:
            raise ValueError("Contest not found.")
        return contest

    def _validate_contest_started(
        self,
        contest: Contest,
    ) -> None:
        now = datetime.now(timezone.utc)
        if contest.start_time > now:
            raise ValueError(
                "Leaderboard is not available before the contest starts."
            )

    def _initialize_scoreboard(
        self,
        participants,
    ) -> dict[int, dict]:
        scoreboard = {}
        for participant in participants:
            scoreboard[participant.id] = {
                "user": participant,
                "total_score": 0,
                "solved_problems": 0,
                "total_penalty": 0,
                "last_accepted_time": None,
                "statistics": {
                    "total_submissions": 0,
                    "accepted_submissions": 0,
                    "wrong_submissions": 0,
                    "compilation_errors": 0,
                    "runtime_errors": 0,
                    "time_limit_exceeded": 0,
                    "memory_limit_exceeded": 0,
                },
                "problem_scores": {},
            }
        return scoreboard

    def _initialize_problem_scores(
        self,
        participants,
        problems,
    ) -> dict[int, dict[int, ProblemScore]]:
        participant_scores = defaultdict(dict)
        for participant in participants:
            for problem in problems:
                participant_scores[
                    participant.id
                ][problem.id] = ProblemScore(
                    problem_id=problem.id,
                    solved=False,
                    score=0,
                    penalty_minutes=0,
                    accepted_submission_id=None,
                    accepted_at_minutes=None,
                    wrong_attempts=0,
                )
        return dict(participant_scores)

