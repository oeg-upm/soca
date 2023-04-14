FROM python:3.10
ENV IN_DOCKER yes
WORKDIR /soca
RUN mkdir src
COPY pyproject.toml pyproject.toml
COPY setup.cfg setup.cfg
COPY ./installer.sh ./installer.sh
COPY ./container_run.sh ./container_run.sh
COPY ./src ./src
RUN pip3 install -e .
RUN python -m nltk.downloader wordnet
RUN python -m nltk.downloader omw-1.4
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader stopwords
RUN ./installer.sh
CMD ./container_run.sh
