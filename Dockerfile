FROM python:3.8.0-alpine
MAINTAINER Chiara Baraglia <c.baraglia@studenti.unipi.it>

ADD . /code
WORKDIR code

RUN pip install -r requirements.txt
RUN python setup.py develop
RUN export FLASK_APP=dice/app


# ENV LANG C.UTF-8
# ENV LC_ALL C.UTF-8
ENV FLASK_APP dice/app.py

EXPOSE 5000

# bind to 0.0.0.0 will make Docker works
CMD ["flask","run","--host", "0.0.0.0"]

