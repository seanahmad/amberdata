FROM python:3.7.7-slim-stretch as builder

# We don't make pyamber installable. It's enough to copy it!
COPY pyamber         /amberdata/pyamber

# install all requirements...
RUN pip install --no-cache-dir pandas==0.25.3 requests==2.23.0 flask==1.1.1

# ----------------------------------------------------------------------------------------------------------------------
FROM builder as production

COPY config           /amberdata/config

# ----------------------------------------------------------------------------------------------------------------------
FROM builder as test
# copy over the tests
COPY test /amberdata/test

# install a bunch of test tools
RUN pip install --no-cache-dir -r /amberdata/test/requirements.txt

