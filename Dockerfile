FROM python:3.11-bullseye

ENV PYTHONUNBUFFERED True
ENV HOME=/opt/repo

WORKDIR ${HOME}

COPY . ${HOME}

RUN pip install pipenv
RUN pipenv requirements --categories packages > ${HOME}/requirements.txt
RUN pip install --no-cache-dir --upgrade -r ${HOME}/requirements.txt
RUN chmod +x ${HOME}/docker-entrypoint.sh

ENTRYPOINT ["/opt/repo/docker-entrypoint.sh"]
