import tempfile

import nox


locations = "src", "tests", "noxfile.py"


def install_with_contraints(session, *args, **kwargs):
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session(python=["3.8"])
def tests(session):
    args = session.posargs or ["--cov"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_contraints(session, "coverage[toml]", "pytest", "pytest-cov", "pytest-flask")
    session.run("pytest", *args)


@nox.session(python=["3.8"])
def lint(session):
    args = session.posargs or locations
    install_with_contraints(session, "flake8", "flake8-import-order")
    session.run("flake8", *args)