

# NVDAPI ![NVDAPI Status](https://codeship.com/projects/de82d210-8acd-0133-0e97-7246c649b408/status?branch=master)

NVDAPI is a JSON REST API project to share the list of vulnerabilities of the [National Vulnerability Database]

It provides a method to list and detail CVEs and some filters/searchs as well.

## Dependencies

- Pip ([How to install pip])
- Virtualenv (```pip install virtualenv```)

## Installation

```sh
git clone https://github.com/Diviei/nvdapi.git
cd nvdapi
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
```

[National Vulnerability Database]: <https://nvd.nist.gov/>
[How to install pip]: <https://pip.pypa.io/en/stable/installing/>
