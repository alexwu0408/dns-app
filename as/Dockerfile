FROM python:3.9-slim

# Set up a working folder and install the pre-reqs
WORKDIR /app

RUN pip install Flask
RUN pip install Flask requests

COPY . .

CMD ["python", "user_server.py"]
