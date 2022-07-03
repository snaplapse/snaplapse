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

## Setting up AWS
Boto3 is the package required to use the AWS SDK for Python
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html

Follow the instructions in the link to install and configure.
For access keys, these can be obtained by logging into using the AWS user provided in discord, then going to security credentials in the top-right, then access keys.
Create a new access key, this should let you use the boto package.
I think as the root user I'm supposed to create other users through the IAM, but using the singular root user is fine for now.

S3 code:
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-examples.html
A lot of the media subsystem is just using these functions to create buckets, upload files, return files.
It will be more fleshed out when I understand more of the desired repo structure.
