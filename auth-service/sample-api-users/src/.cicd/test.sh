#!/bin/bash -e 


if [ "${TEST_TARGET:-}" = "INTEGRATION" ]; then
    # Execute your command here
    /usr/src/app/.venv/bin/gunicorn manage:app
else
    ## pytest
    python -m pytest "src/tests" --junitxml=report.xml

    ## Coverage
    python -m pytest "src/tests" -p no:warnings --cov="src" --cov-report xml


    ## Linting
    flake8 src --extend-ignore E221
    # black src --check
    # isort src --check

    ## Security
    # bandit -c .bandit.yml -r .
fi

