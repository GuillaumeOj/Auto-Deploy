import os
import subprocess

from webhooks import app
from webhooks.hooks import WrongEvent
from webhooks.hooks import WrongRef
from webhooks.hooks import WrongRepository


def push_on_master(request):
    repositories_config = app.config["REPOSITORIES_CONFIG"]

    main_dir = repositories_config.setdefault("main_dir", "")
    local_repositories = repositories_config.setdefault("repositories", [])

    headers = request.headers
    event = headers.setdefault("X-GitHub-Event", "")

    payload = request.json()

    if event == "push":
        ref = payload["ref"]
        repository = payload["repository"]
        repository_name = repository["name"].lower()
        django_app = repository.setdefault("django", default=False)

        for local_repository in local_repositories:
            main_branch = local_repository.setdefault(
                "main_branch", app.config["DEFAULT_BRANCH"]
            )
            if repository_name == local_repository["name"]:
                if main_branch in ref:
                    run_args = [
                        os.path.join(app.config["CURRENT_DIR"], "update_repos.sh"),
                        "-d",
                        os.path.join(main_dir, local_repository["directory"]),
                        "-r",
                        repository_name,
                    ]

                    if django_app:
                        run_args.extend(["-t", "django"])

                    subprocess.run(run_args, check=True)
                else:
                    raise WrongRef()

        raise WrongRepository()

    raise WrongEvent()
