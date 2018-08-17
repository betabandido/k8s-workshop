FROM python:3-alpine
EXPOSE 5000
RUN pip install Flask
WORKDIR /app
COPY main.py .
ENTRYPOINT ["python"]
CMD ["main.py"]
