import os
import re
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

        ref_is_deleted = payload["deleted"]
        commiter_names = [commit["commiter"]["name"] for commit in payload["commits"]]
        commiter_is_not_bot = (
            True if re.finditer(r"bot", ":".join(commiter_names)) else False
        )

        if repository_name == local_repository["name"]:
            # Two cases :
            # 1. The user push directly on master so => ref in the payload is the
            #    main_branch and the commiter is not a bot
            # 2. Pushed from a pull-request so => ref in the payload is not the
            #    main_branch but the ref_is_deleted
            if (main_branch in ref and commiter_is_not_bot) or ref_is_deleted:
                run_args = [
                    os.path.join(app.config["CURRENT_DIR"], "update_repos.sh"),
                    "-d",
                    os.path.join(main_dir, local_repository["directory"]),
                    "-r",
                    repository_name,
                ]

                # TODO: this part must be improve by using a config file in the
                # repository with the commands which must be runned after the update
                if local_repository.setdefault("django", False):
                    run_args.extend(["-t", "django"])
                    result = subprocess.run(run_args, check=True)
                    app.logger.info(result)
