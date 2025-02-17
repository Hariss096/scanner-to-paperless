# HP Scanner to Paperless NGX

## Tested with HP Deskjet 2700 All in one

### Local setup

- To install dependencies:
    - to create virtual env in root dir, make sure poetry is configured accordingly:
        `poetry config virtualenvs.in-project true`
    - creates a virtual environment and installs dependencies there: `poetry install`


- Run directly: `poetry run streamlit run app.py`
- Run via docker: `docker compose up`


- Setup pre-commit: `poetry run pre-commit install`
