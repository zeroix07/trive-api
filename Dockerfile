FROM python:3.12-slim
ENV PYTHONBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
RUN pip install -r requirements.txt
CMD ["python", "app.py"]