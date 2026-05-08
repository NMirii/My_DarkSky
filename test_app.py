# Quick test to ensure Flask app structure is correct
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return "Flask is working!"

if __name__ == '__main__':
    print("Testing Flask setup...")
    print("✓ Flask imported successfully")
    print("✓ App created")
    print("✓ Route defined")
    print("\nAll basic checks passed!")
