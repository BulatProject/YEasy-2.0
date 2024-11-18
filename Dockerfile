FROM public.ecr.aws/docker/library/python:slim-buster
RUN apt-get -y update && apt-get install -y ffmpeg
WORKDIR /YEasy
RUN pip install virtualenv
ENV VIRTUAL_ENV=./venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
EXPOSE  80/tcp