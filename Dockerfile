FROM python:3-onbuild
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD [ "python", "api.py" ]