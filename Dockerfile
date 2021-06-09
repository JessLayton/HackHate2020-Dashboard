# "FROM" starts us out from this Ubuntu-based image
# https://github.com/tiangolo/uwsgi-nginx-flask-docker/blob/master/python3.7/Dockerfile

FROM tiangolo/uwsgi-nginx-flask:python3.7

# Optionally, install some typical packages used for building and network debugging.
RUN apt-get update

# Update to the latest PIP
RUN pip3 install --upgrade pip

# Our application code will exist in the /app directory,
# so set the current working directory to that
WORKDIR /app

# Backup the default app files.  You could also delete these
RUN rm main.py uwsgi.ini


# Copy our files into the current working directory WORKDIR
COPY ./src/ ./

# install our dependencies
RUN  pip3 install -r requirements.txt