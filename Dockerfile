# 1. Use an official Python image
FROM python:3.9-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy your requirements and install them
COPY requirements.txt .
RUN pip install -r requirements.txt

# 4. Copy the rest of your code (model.pkl, app.py, etc.)
COPY . .

# 5. Tell Docker to run Streamlit when the container starts
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]