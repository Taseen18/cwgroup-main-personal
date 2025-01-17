FROM registry.access.redhat.com/ubi8/python-311

USER root
RUN yum update -y && yum install -y \
    gcc \
    libpq-devel \
    python3-devel \
    sqlite-devel \
    && yum clean all

USER 1001
WORKDIR /opt/app-root/src

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

CMD gunicorn cwgroup-main.wsgi:application --bind 0.0.0.0:$PORT
