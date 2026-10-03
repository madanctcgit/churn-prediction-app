FROM python:3.12-slim


# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 7860

# Run Flask app
#CMD ["python", "app.py"]
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7860", "app:SuperKart"]
