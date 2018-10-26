# == Disclaimer ================================================================
# We are running the project's Docker image only for **local development
# purpose** (and not production + development). This image is not supposed to be
# working in OpenShift or other platforms that assign a random non-privileged
# user ID to run a container. Hence, when working with this image, it's more
# comfortable to rely on an existing user (when you log in the container, etc.)
# than a random one activated via an `entrypoint` (that is therefore not
# required here).
# ==============================================================================
FROM fundocker/edxapp:hawthorn.1-2.0.1

ARG UID=1000
ARG GID=1000

# Switch back to a priviledged user to perform base installation
USER root:root

# Add the non-privileged user that will run the application
RUN groupadd --gid ${GID} edxapp && \
    useradd --uid ${UID} --gid ${GID} --home-dir /edx edxapp

# Allow the edx user to create files in /edx/var (required to perform database
# migrations)
RUN mkdir /edx/var && \
    chown edxapp:edxapp /edx/var

# Override LMS settings used for development (with xapi enabled)
COPY ./docker/config/lms/docker_run_development.py /config/lms/

# Copy the app to the working directory (requires an existing system user)
COPY --chown=edxapp:edxapp . /edx/app/xapi/

# Install development dependencies in a virtualenv
RUN pip install --no-cache-dir --src /usr/local/src -e /edx/app/xapi

# FIXME: as mentionned in fun-platform and edx-platform bug tracker, this
# webpack-stats.json is required both in production and development in a static
# directory 😢
RUN mkdir /edx/app/edxapp/staticfiles && \
    cp /edx/app/edxapp/edx-platform/common/static/webpack-stats.json /edx/app/edxapp/staticfiles/

# Install dockerize to wait for mysql before running the container command
# (and prevent connection issues)
ENV DOCKERIZE_VERSION v0.6.1
RUN python -c "import requests;open('dockerize-linux-amd64.tar.gz', 'wb').write(requests.get('https://github.com/jwilder/dockerize/releases/download/${DOCKERIZE_VERSION}/dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz', allow_redirects=True).content)" && \
    tar -C /usr/local/bin -xzvf dockerize-linux-amd64.tar.gz && \
    rm dockerize-linux-amd64.tar.gz

# Download a demo course in the container itself so that we can import if
# further without having to deal with volume permissions, etc.
ARG DEMO_COURSE_URL=https://github.com/edx/edx-demo-course/archive/open-release/hawthorn.1.tar.gz
RUN mkdir -p /edx/demo/course && \
    python -c "import requests;open('/edx/demo/course.tgz', 'wb').write(requests.get('${DEMO_COURSE_URL}', allow_redirects=True).content)" && \
    cd /edx/demo && \
    tar xzf course.tgz -C ./course --strip-components=1

# Give running user write permissions for the data directory where courses will
# be imported
RUN mkdir -p /edx/app/edxapp/data && \
    chown edxapp:edxapp /edx/app/edxapp/data

# Switch to an un-privileged user matching the host user to prevent permission
# issues with volumes (host folders)
USER ${UID}:${GID}
