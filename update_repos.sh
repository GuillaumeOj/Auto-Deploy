#!/usr/bin/bash

while getopts "d:r:t" option; do
	case ${option} in
		d) 
			directory_path=${OPTARG}
			;;
		r)
			repository_name=${OPTARG}
			;;
		t)
			application_type=${OPTARG}
			;;
	esac
done

if [ -z $DEFAULT_BRANCH ]
then
	export DEFAULT_BRANCH="master"
fi

if [ -e $directory_path ] && [ -d $directory_path ]
then
	cd $directory_path
else
	echo "$(date): the given directory is incorrect => $directory_path"
	exit 1
fi

if [ -z $repository_name ]
then
	echo "$(date): the repository name is empty."
	exit 1
fi

if [ -e "poetry.lock" ]
then
	dependencies_diff=$(git diff origin/$DEFAULT_BRANCH poetry.lock) 
else
	echo "$(date): lock file for dependencies is missing."
	exit 1
fi

echo "==================================================================="
echo "$(date): Starting update"

echo "$(date): Update the repository: $repository_name"
echo "$(date): $(git pull --rebase)"

if [ -n $dependencies_diff ]
then
	echo "$(date): $(poetry install)"
fi

if [ $application_type == "django" ]
then
	echo "$(date): $(poetry shell)"
	echo "$(date): $(python manage.py migrate)"
	echo "$(date): $(python manage.py collectstatic --noinput)"
	echo "$(date): $(deactivate)"
fi

echo "$(date): $(supervisorctl restart $repository_name)"

echo "$(date): End of update"
echo "==================================================================="
