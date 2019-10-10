FROM alpine:3.10 as builder

WORKDIR /app

COPY requirements.txt /app

RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip

#RUN pip3 --no-cache-dir install -r requirements.txt
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps


FROM builder as code_files

COPY . /app

EXPOSE 5000

#CMD ["gunicorn", "wsgi:app"]
CMD ["gunicorn" , "-b", "0.0.0.0:5000", "wsgi:app"]
