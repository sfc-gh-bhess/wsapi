FROM python:3.10
EXPOSE 8080
WORKDIR /app
COPY src/requirements.txt .
RUN pip3 install -r requirements.txt
RUN pip3 uninstall oscrypto -y
RUN pip3 install oscrypto@git+https://github.com/wbond/oscrypto.git@d5f3437ed24257895ae1edd9e503cfb352e635a8
COPY src/. .
CMD ["fastapi", "run", "app.py", "--port", "8080"]
