## Base FastAPI template
- oauth2 ready (using [FastAPI Users](https://fastapi-users.github.io/fastapi-users))
- send email (using [FastApi-MAIL](https://sabuhish.github.io/fastapi-mail/))

## Documentation
To view docs, first install all requirements:
```sh
pip install -r requirements/local.txt
```
Then serve the docs locally with:
```sh
mkdocs serve -a localhost:8080 -f docs/mkdocs.yml
```