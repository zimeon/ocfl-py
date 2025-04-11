coverage run --source=ocfl -m pytest
coverage report
coverage html
echo -n "See htmlcov/index.html for details."
