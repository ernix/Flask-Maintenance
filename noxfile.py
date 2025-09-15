import nox


@nox.session(python="3.13")
def lint(session):
    session.install("build", "twine")
    session.run("python", "-m", "build", external=True)
    session.run("python", "-m", "twine", "check", "dist/*")


@nox.session(python=["3.11", "3.12", "3.13"])
def tests(session):
    """Run the test suite"""
    session.install("flask", "mock", "pytest", "pytest-cov")
    session.install("-e", ".")
    session.run("pytest", "--cov=flask_maintenance", "--cov-report=")
    session.run("coverage", "report", "--show-missing", "--fail-under=100")
