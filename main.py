from flask import Flask
import os
from app import app

# Make sure uploads directory exists
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Use the PORT environment variable that Replit provides
port = int(os.environ.get("PORT", 8080))

if __name__ == "__main__":
    # The '0.0.0.0' is critical - it allows external connections
    app.run(host='0.0.0.0', port=port)
    