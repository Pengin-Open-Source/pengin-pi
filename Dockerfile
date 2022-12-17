FROM tiangolo/uwsgi-nginx-flask:latest

ENV UWSGI_CHEAPER 4
ENV UWSGI_PROCESSES 64
ENV NGINX_MAX_UPLOAD 1m
ENV NGINX_WORKER_PROCESSES 1
ENV NGINX_WORKER_CONNECTIONS 2048
ENV STATIC_PATH /pengin-pie/app/static
ENV UWSGI_INI /pengin-pie/uwsgi.ini
ENV LISTEN_PORT 5000
EXPOSE 5000
# Set the working directory in the container
WORKDIR /pengin-pie

# Copy the dependencies file to the working directory

COPY ./app /pengin-pie/app
COPY ./app/templates /pengin-pie/app/templates
COPY ./requirements.txt /pengin-pie/requirements.txt

# Install any dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . /pengin-pie