import os
import subprocess

from webhooks import app


def push_master(request):
    repositories_config = app.config["REPOSITORIES_CONFIG"]

    main_dir = repositories_config.setdefault("main_dir", "")
    local_repositories = repositories_config.setdefault("repositories", [])

    payload = request.get_json()

    ref = payload.setdefault("ref", "")

    repository_name = payload["repository"].setdefault("name", "").lower()

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

                if local_repository.setdefault("django", False):
                    run_args.extend(["-t", "django"])
                    result = subprocess.run(run_args, check=True)
                    app.logger.info(result)
