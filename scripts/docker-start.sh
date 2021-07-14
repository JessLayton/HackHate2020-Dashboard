#!/bin/sh
# below needs replacing
docker build -t pythondemo .
docker run --name demo -p 80:80 pythondemo