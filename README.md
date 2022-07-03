# SnapLapse

## Setup
Install pyenv
https://github.com/pyenv/pyenv

Install python
```sh
pyenv install 3.10.4
```

Setup pipenv
```sh
# macOS
brew install pipenv

# Windows

# Install dependencies
pipenv --python 3.10.4 install --dev

# Launch virtual environment
pipenv shell

# Install pre-commit hooks
pre-commit install
```

## Run
```sh
# Launch virtual environment
pipenv shell

# Run migrations
python manage.py migrate

# Run the server
python manage.py runserver
```
