FROM python:3.6.2-alpine3.6
ENV PYTHONBUFFERED 1

# Install pipenv
RUN pip install pipenv

# Add new user to run the whole thing as non-root
RUN addgroup -S app
RUN adduser -G app -h /app -D app

# Copy Pipfile and install system-wide
# We're installing system-wide, because we currently have problems
# correctly using the entrypoint.sh, while activating the virtual environment
COPY Pipfile /app
WORKDIR /app
RUN pipenv install --system

# Change to user and copy code
USER app
COPY . /app

ENTRYPOINT ["/app/entrypoint.sh"]
