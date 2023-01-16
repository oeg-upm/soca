FROM 3.9.16-alpine3.16
RUN pip3 install -e .
CMD [ "python", "./__main__.py" ]