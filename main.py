import os
from flask import Flask, render_template
from app import create_app

app = create_app()

if __name__ == "__main__":    
    app.run(port=8000) # pass debug=True parameter in development