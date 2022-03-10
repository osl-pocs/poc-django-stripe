# ref: https://github.com/mamba-org/micromamba-docker/blob/main/Dockerfile

FROM condaforge/mambaforge:latest

LABEL maintainer="Ivan Ogasawara <ivan.ogasawara@gmail.com>"
LABEL org.opencontainers.image.title="PoC"
LABEL org.opencontainers.image.authors="PoC Team"
LABEL org.opencontainers.image.source="https://github.com/osl-incubator/poc-django-stripe"
LABEL org.opencontainers.image.version="latest"
LABEL org.opencontainers.image.description="PoC Django Stripe"
LABEL org.osl.poc_django_stripe.version="latest"

# it is the default, but using it here to have it explicitly
USER root

SHELL ["/bin/bash", "-c"]
# Use bash in Dockerfile RUN commands and make sure bashrc is sourced when
# executing commands with /bin/bash -c
# Needed to have the micromamba activate command configured etc.

ENV ENV_NAME=poc-django-stripe
ENV DEBIAN_FRONTEND=noninteractive
ARG UID=1000  # default value 1000
ARG GID=1000  # default value 1000

RUN apt-get update -y \
  && apt-get install -y \
    build-essential \
    zip \
    make \
    cron \
    curl \
    wget \
    sudo \
    tini \
  && rm -rf /var/lib/apt/lists/* \
    /var/cache/apt/archives \
    /tmp/* \
  && addgroup --gid ${GID} poc \
  && useradd --uid ${UID} --gid ${GID} -ms /bin/bash poc \
  && mkdir -p /opt/services \
  && chmod -R a+rwx /opt/conda /opt/services/ \
  && export ENV_NAME="$ENV_NAME" \
  && echo "poc ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/poc \
  && chmod 0440 /etc/sudoers.d/poc

USER poc

WORKDIR /opt/services/

COPY --chown=poc:poc ./conda/ /tmp/conda

ENV PATH /opt/conda/envs/$ENV_NAME/bin:$PATH
ENV PYTHONPATH='/opt/services/poc-django-stripe:/opt/services/'

RUN mamba env create -n $ENV_NAME --file /tmp/conda/dev.yaml \
  && conda clean --all \
  && find /opt/conda/ -type f,l -name '*.a' -delete \
  && find /opt/conda/ -type f,l -name '*.pyc' -delete \
  && find /opt/conda/ -type f,l -name '*.js.map' -delete \
  && rm -rf /opt/conda/pkgs /tmp/*

# note: keeping it to the end of the recipes helps to avoid rebuilding the
#       image after every change.
# COPY --chown=poc:poc . /opt/services/

COPY --chown=poc:poc docker/entrypoint.sh /opt/entrypoint.sh
COPY --chown=poc:poc docker/superset/superset.sh /opt/superset.sh

RUN chmod +x /opt/entrypoint.sh \
  && echo "source /opt/entrypoint.sh" > ~/.bashrc

ENTRYPOINT ["tini", "--", "/opt/entrypoint.sh"]
CMD ["/opt/superset.sh"]
