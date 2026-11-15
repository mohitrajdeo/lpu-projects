FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir fastapi uvicorn scikit-learn numpy joblib pydantic
COPY . /app
EXPOSE 5002
CMD ["python", "src/service.py"]

