FROM python:3.9.7-alpine3.14 as Base

EXPOSE 8000

WORKDIR /app

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories && \
  apk add nodejs

COPY requirements.txt requirements.txt

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
  pip install --upgrade pip && \
  pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD [ "uvicorn" ,"main:app","--host", "0.0.0.0"]