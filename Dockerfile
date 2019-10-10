FROM alpine:3.10

RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip

WORKDIR /app

COPY . /app

#RUN pip3 --no-cache-dir install -r requirements.txt
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

#RUN apk add --no-cache bash

EXPOSE 5000

#RUN ["chmod", "+x", "./wait-for-it.sh"]

#CMD ["gunicorn", "wsgi:app"]
CMD ["gunicorn" , "-b", "0.0.0.0:5000", "wsgi:app"]
