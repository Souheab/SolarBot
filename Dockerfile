FROM python:3.12.8-bullseye
WORKDIR /app
COPY . .
RUN python -m venv .venv
RUN . .venv/bin/activate
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
