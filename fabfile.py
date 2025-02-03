from fabric import task


@task
def runserver(
    c, host='0.0.0.0', port='8000',
    env_file='.env'
):
    c.run(f'uvicorn main:app --host {host} --port {port} --reload '
          f'--env-file {env_file}')


@task
def makemigrations(
    c, migration='init'
):
    c.run(f'alembic revision --autogenerate -m "{migration}"')


@task
def migrate(c):
    c.run('alembic upgrade head')
