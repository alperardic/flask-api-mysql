FROM sefaydinelli/flask-app-mysql:base-image-alpine
WORKDIR /app
COPY . ./
EXPOSE 8080
ENTRYPOINT ["python3", "flask_app.py"]