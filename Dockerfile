FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
RUN python3 -m pip install requests bs4 pydantic typing
COPY ./app /app