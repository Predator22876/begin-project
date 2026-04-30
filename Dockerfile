FROM python:3.12.8

RUN echo ls
WORKDIR /app
RUN echo ls

COPY requirenments.txt requirenments.txt
RUN pip install -r requirenments.txt

COPY . .


# CMD ["python", "-m", "src.main"]
CMD alembic upgrade head; python -m src.main