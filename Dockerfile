# Use official Python 3.10 image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
RUN pip install -r requirements.txt

# Expose port (Render assigns PORT)
EXPOSE 7860

# Set environment variables for Render
ENV PORT=7860

# Start the app
CMD ["python", "app.py"]
