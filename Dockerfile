# Set the base image to Ubuntu
FROM continuumio/miniconda3:4.8.2 as builder

# File Author / Maintainer
MAINTAINER Thomas Schmelzer "thomas.schmelzer@gmail.com"

# We don't make pyamber installable. It's enough to copy it!
COPY pyamber         /amberdata/pyamber

# install all requirements...
RUN conda install -y -c conda-forge nomkl pandas=0.25.3 requests=2.23.0 flask=1.1.1 && \
    conda clean -y --all

WORKDIR amberdata
# ----------------------------------------------------------------------------------------------------------------------
FROM builder as production

COPY config           /amberdata/config

# ----------------------------------------------------------------------------------------------------------------------
FROM builder as test

# install a bunch of test tools
RUN pip install --no-cache-dir httpretty pytest pytest-cov pytest-html requests-mock

CMD py.test --cov=pyamber  --cov-report html:artifacts/html-coverage --cov-report term --html=artifacts/html-report/report.html /amberdata/test

# copy over the tests
COPY test /amberdata/test

