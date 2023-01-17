FROM python:3.9
WORKDIR /soca
RUN mkdir src
COPY pyproject.toml pyproject.toml
COPY setup.cfg setup.cfg
COPY ./src ./src
RUN pip3 install -e .
WORKDIR /soca/src/soca
CMD [ "soca", "-h" ]
