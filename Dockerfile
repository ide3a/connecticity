FROM ubuntu:20.04

# Setup python and java and base system
# ------------------------------------------------------------------------------
ENV DEBIAN_FRONTEND noninteractive
# ENV LANG=en_US.UTF-8

# General general tools
# ------------------------------------------------------------------------------
RUN apt-get update && \
      apt-get install -y unzip cmake wget

# Install Python 3.8
# ------------------------------------------------------------------------------
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 --no-cache-dir install --upgrade pip \
  && rm -rf /var/lib/apt/lists/*

# Install OpenJDK-11
# ------------------------------------------------------------------------------
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get install -y ant && \
    apt-get clean;
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/

# Install SUMO
# ------------------------------------------------------------------------------
RUN apt-get install -y software-properties-common && \
  add-apt-repository ppa:sumo/stable && \
  apt-get update && \
  apt-get install -y sumo sumo-tools sumo-doc

# Install swmm
# ------------------------------------------------------------------------------
RUN wget https://www.epa.gov/sites/default/files/2020-08/swmm51015_engine.zip
RUN unzip swmm51015_engine.zip && \
      mkdir swmm51015_engine/build && \
      cd swmm51015_engine/build && \
      cmake .. && \
      cmake --build . --config Release

# Install Python libraries
# ------------------------------------------------------------------------------
COPY requirements.txt /.
RUN  python3 -m pip install -r /requirements.txt

# Temporary: Install hydro privacy dependencies
COPY hydro_privacy/requirements.txt /hydro_privacy_requirements.txt
RUN  python3 -m pip install -r /hydro_privacy_requirements.txt

WORKDIR /connecticity/client

# CMD jupyter lab --allow-root
