
FROM python:3.10-windowsservercore-1809 


WORKDIR /user/src/app 


COPY requirements.txt ./ 
RUN pip install --no-cache-dir -r requirements.txt --user 
COPY . . 


ENTRYPOINT ["python", "./runserver.py"] 

EXPOSE 5000