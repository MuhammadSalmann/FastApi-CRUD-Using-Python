Create Virtual Environment
-> python -m venv venv

Activate the virtual environment
On Windows: venv\Scripts\activate

Install Dependdencies (you can also do this manually by installing each dependecy)
-> pip freeze > requirements.txt

Run the Server
-> uvicorn app.main:app --reload
