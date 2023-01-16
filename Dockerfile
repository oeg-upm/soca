FROM python:3.9
WORKDIR /soca
RUN mkdir src
COPY pyproject.toml pyproject.toml
COPY setup.cfg setup.cfg
COPY ./src ./src
RUN pip3 install -e .
CMD [ "python", "./src/soca/__main__.py" ]
