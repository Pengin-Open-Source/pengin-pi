# start by pulling the python image
FROM python:3.10-alpine

# source: awsgeek.com
EXPOSE 5000/tcp

# copy the requirements file into the image
COPY ./requirements.txt pengin-pie/requirements.txt

# switch working directory
WORKDIR /pengin-pie

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /pengin-pie

# configure the container to run in an executed manner
# ENTRYPOINT [ "flask" ]

CMD [ "flask", "run", "--host", "0.0.0.0"]