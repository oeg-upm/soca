FROM python:3.9
RUN pip3 install -e .
CMD [ "python", "./__main__.py" ]
