CALL .\myvenv\Scripts\activate
set FLASK_APP=src/main.py
set FLASK_ENV=development
flask run -h 0.0.0.0 -p 5004

