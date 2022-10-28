FROM python:3.9-alpine as Base

EXPOSE 8000

WORKDIR /app

ARG APK_REGISTRY

RUN if [[ -n "${APK_REGISTRY}" ]]; then sed -i "s/${APK_REGISTRY}/g" /etc/apk/repositories; fi && \
    apk add nodejs

COPY requirements.txt requirements.txt

ARG PIP_REGISTRY

RUN if [[ -n "${PIP_REGISTRY}" ]]; then pip config set global.index-url ${PIP_REGISTRY}; fi && \
    pip install --upgrade pip && \
    pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD [ "uvicorn" ,"main:app","--host", "0.0.0.0", "--port", "8000"]