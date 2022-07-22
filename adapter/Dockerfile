FROM python:3
ADD script.py requirements.txt /
#RUN apt-get -qq update && apt-get -qq install -y iputils-ping #for testing
RUN pip3 install -r requirements.txt
CMD [ "python", "-u", "./script.py" ]
