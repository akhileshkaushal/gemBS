FROM ubuntu:xenial
MAINTAINER Simon Heath (simon.heath@gmail.com)
RUN apt-get update
RUN apt-get install -y libpng-dev uuid-dev libmysqlclient-dev
RUN apt-get install -y python3 build-essential git python3-pip wget pigz
RUN apt-get install -y zlib1g-dev libbz2-dev gsl-bin libgsl0-dev
RUN apt-get install -y libncurses5-dev liblzma-dev libssl-dev libcurl4-openssl-dev
RUN pip3 install matplotlib multiprocess
RUN mkdir /usr/local/build; cd /usr/local/build
RUN git clone --recursive https://github.com/heathsc/gemBS.git
RUN (cd gemBS; python3 setup.py install)
RUN rm -rf gemBS && cd && rmdir /usr/local/build
RUN echo "cd /home;/usr/local/bin/gemBS \$@" > start.sh
ENTRYPOINT ["/bin/bash", "start.sh"]
