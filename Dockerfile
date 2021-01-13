FROM python:3.8.7-buster

RUN pip install XNAT==0.3.25
ADD download_egd.py /

ENTRYPOINT ["python", "-u", "download_egd.py"]
