FROM python:3.13-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install uvicorn

EXPOSE 8080

CMD ["python", "level_2_agent.py"]
