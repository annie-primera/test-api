FROM python:3-slim-bullseye as builder
WORKDIR /app
COPY . ./
COPY ./requirements.txt .
RUN pip install -r requirements.txt

FROM builder as runner
EXPOSE 8003
CMD ["python", "-m", "main"]