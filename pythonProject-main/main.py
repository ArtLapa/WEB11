from fastapi import FastApi

app = FastApi()


@app.get('/')
def index():
    return ('message': 'Todo Application')