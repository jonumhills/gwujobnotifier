FROM python:3.9-slim
WORKDIR /gwujobnotifier
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5001
ENV FLASK_APP=jobnotifier.py
CMD ["flask", "run", "--host=0.0.0.0"]
