import json
import os
from pprint import pprint
from typing import List, Dict
import hashlib

from canvasapi import Canvas
from canvasapi.quiz import QuizSubmissionQuestion, QuizSubmission
from environs import Env
from git import Repo

# problemset specific imports
from pyramid import print_pyramid
from fibonacci import last_8, SummableSequence, optimized_fibonacci
from test_pset import capture_print

def get_answers(questions: List[QuizSubmissionQuestion]) -> List[Dict]:
    """Creates answers for Canvas quiz questions"""
    # Formulate your answers - see docs for QuizSubmission.answer_submission_questions below
    # It should be a list of dicts, one per q, each with an 'id' and 'answer' field
    # The format of the 'answer' field depends on the question type
    # You are responsible for collating questions with the functions to call - do not hard code
    
    # submission list
    submission = []

    # answering fib/summable questions
    answers = {}

    # optimised fibonacci questions
    answers["fib_100000"] = last_8(optimized_fibonacci(100000))
    answers["fib_234202"] = last_8(optimized_fibonacci(234202))
    
    # summable questions
    seq = SummableSequence(0, 1)
    answers["fib_234202"] =last_8(seq(100000))

    seq = SummableSequence(5, 7, 11)
    answers["fib_234202"] = last_8(seq(100000))

    seq = SummableSequence(5, 98, 7, 35, 2)
    answers["fib_234202"] = last_8(seq(603))

    seq = SummableSequence(8, 9, 99)
    answers["fib_234202"] = last_8(seq(141515))

    tmp = {'id': questions[0].id, "answers": answers}
    submission.append(tmp)

    # answering pyramid questions
    answers = {}
    
    # anwser for pyramid_24
    with capture_print() as std:
        print_pyramid(24)
    std.seek(0)
    output = std.read()
    answers["pyramid_24"] = hashlib.sha256(output.encode()).hexdigest()

    # anwser for pyramid_53
    with capture_print() as std:
        print_pyramid(53)
    std.seek(0)
    output = std.read()
    answers["pyramid_53"] = hashlib.sha256(output.encode()).hexdigest()

    tmp = {'id': questions[1].id, "answers": answers}

    submission.append(tmp)

    # answering time question
    tmp = {'id': questions[2].id, "answers": 3268}
    submission.append(tmp)

    # eg {"id": questions[0].id, "answer": {key: some_func(key) for key in questions[0].answer.keys()}}
    return submission


def get_submission_comments(repo: Repo, qsubmission: QuizSubmission) -> Dict:
    """Get some info about this submission"""
    return dict(
        hexsha=repo.head.commit.hexsha[:8],
        submitted_from=repo.remotes.origin.url,
        dt=repo.head.commit.committed_datetime.isoformat(),
        branch=os.environ.get("TRAVIS_BRANCH", None),  # repo.active_branch.name,
        is_dirty=repo.is_dirty(),
        quiz_submission_id=qsubmission.id,
        quiz_attempt=qsubmission.attempt,
        travis_url=os.environ.get("TRAVIS_BUILD_WEB_URL", None),
    )


if __name__ == "__main__":

    repo = Repo(".")

    # Load environment
    env = Env()

    course_id = env.int("CANVAS_COURSE_ID")
    assignment_id = env.int("CANVAS_ASSIGNMENT_ID")
    quiz_id = env.int("CANVAS_QUIZ_ID")
    as_user_id = env.int("CANVAS_AS_USER_ID", 0)  # Optional - for test student

    if as_user_id:
        masquerade = dict(as_user_id=as_user_id)
    else:
        masquerade = {}

    if repo.is_dirty() and not env.bool("ALLOW_DIRTY", False):
        raise RuntimeError(
            "Must submit from a clean working directory - commit your code and rerun"
        )

    # Load canvas objects
    canvas = Canvas(env.str("CANVAS_URL"), env.str("CANVAS_TOKEN"))
    course = canvas.get_course(course_id, **masquerade)
    assignment = course.get_assignment(assignment_id, **masquerade)
    quiz = course.get_quiz(quiz_id, **masquerade)

    # Begin submissions
    url = "https://github.com/csci-e-29/{}/commit/{}".format(
        os.path.basename(repo.working_dir), repo.head.commit.hexsha
    )  # you MUST push to the classroom org, even if CI/CD runs elsewhere (you can push anytime before peer review begins)

    qsubmission = None
    try:
        # Attempt quiz submission first - only submit assignment if successful
        qsubmission = quiz.create_submission(**masquerade)
        questions = qsubmission.get_submission_questions(**masquerade)

        # Get some basic info to help develop
        for q in questions:
            print("{} - {}".format(q.question_name, q.question_text.split("\n", 1)[0]))

            # MC and some q's have 'answers' not 'answer'
            pprint(
                {
                    k: getattr(q, k, None)
                    for k in ["question_type", "id", "answer", "answers"]
                }
            )

            print()

        # Submit your answers
        answers = get_answers(questions)
        pprint(answers)
        responses = qsubmission.answer_submission_questions(
            quiz_questions=answers, **masquerade
        )

    finally:
        if qsubmission is not None:
            completed = qsubmission.complete(**masquerade)

            # Only submit assignment if quiz finished successfully
            submission = assignment.submit(
                dict(
                    submission_type="online_url",
                    url=url,
                ),
                comment=dict(
                    text_comment=json.dumps(get_submission_comments(repo, qsubmission))
                ),
                **masquerade,
            )

    pass
