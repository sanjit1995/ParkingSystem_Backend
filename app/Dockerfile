FROM python:3.7
RUN rm -rf /app
COPY . /app
RUN pip install -r ./app/requirements.txt
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","7000"]