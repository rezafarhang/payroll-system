FROM python:3.9-slim-bullseye
RUN apt-get update
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY payrollsystem /app
RUN apt-get update \
	&& apt-get install -y gdal-bin \
	&& apt-get install -y python3-gdal \
    && pip install -r requirements.txt
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]