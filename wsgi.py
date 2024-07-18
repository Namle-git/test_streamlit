from api import flask_app, streamlit_app
import multiprocessing

def app(environ, start_response):
    path = environ.get('PATH_INFO', '').lstrip('/')
    if path.startswith('api/'):
        return flask_app(environ, start_response)
    return streamlit_app()(environ, start_response)

if __name__ == '__main__':
    streamlit_process = multiprocessing.Process(target=streamlit_app)
    streamlit_process.start()
    flask_app.run()
