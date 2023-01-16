FROM python:3.9
WORKDIR /soca
COPY pyproject.toml .
COPY ./src ./src
RUN pip3 install -e .
CMD [ "python", "./__main__.py" ]
