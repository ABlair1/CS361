import os
from flask import Flask, render_template
from app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    
    app.run(port=port, debug=True) # debug=True will reload app when app code is changed