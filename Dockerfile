FROM python:3.6.2
ADD . .
RUN pip install -r requirements.txt
CMD python -u run.py
