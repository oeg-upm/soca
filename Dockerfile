FROM python:3.9
WORKDIR /home
COPY ./configFiles/.soca    ./.soca
COPY ./configFiles/.somef ./.somef
WORKDIR /soca
RUN mkdir src
COPY pyproject.toml pyproject.toml
COPY setup.cfg setup.cfg
COPY ./installer.sh ./installer.sh
COPY ./src ./src
RUN pip3 install -e .
CMD ./installer.sh
