FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app

EXPOSE 8000

COPY . .

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install -r requirements.txt

CMD [ "uvicorn" ,"main:app","--host", "0.0.0.0"]