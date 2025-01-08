from wsgiref.simple_server import make_server
from datetime import datetime
from dateutil import tz
import json

# WSGI main application function
def application(environ, start_response):
    # Handles all incoming HTTP requests.
    path = environ['PATH_INFO']  # Get the requested URL path
    method = environ['REQUEST_METHOD']  # Get the HTTP method

    # Route the requests to appropriate handlers
    if path == '/' and method == 'GET':
        return handle_get_root(environ, start_response)
    elif path.startswith('/') and method == 'GET':
        return handle_get_timezone(environ, start_response)
    elif path == '/api/v1/time' and method == 'POST':
        return handle_post_time(environ, start_response)
    elif path == '/api/v1/date' and method == 'POST':
        return handle_post_date(environ, start_response)
    elif path == '/api/v1/datediff' and method == 'POST':
        return handle_post_datediff(environ, start_response)
    else:
        # Handle invalid routes
        status = '404 Not Found'
        headers = [('Content-Type', 'text/plain')]
        start_response(status, headers)
        return [b'Not Found\n']

# Handle GET /
def handle_get_root(environ, start_response):
    # Returns the current server time in HTML format.
    now = datetime.now()
    server_tz = tz.gettz()  # Get the server's timezone
    now_server_time = now.astimezone(server_tz)
    html = f"<h1>Current Server Time: {now_server_time.strftime('%Y-%m-%d %H:%M:%S %z')}</h1>"
    status = '200 OK'
    headers = [('Content-Type', 'text/html')]
    start_response(status, headers)
    return [html.encode('utf-8')]

# Handle GET /<tz_name>
def handle_get_timezone(environ, start_response):
    # Returns the current time in the specified timezone.
    try:
        tz_name = environ['PATH_INFO'][1:]  # Extract timezone name from URL
        tz_obj = tz.gettz(tz_name)  # Get timezone object
        if not tz_obj:
            raise ValueError(f"Invalid timezone '{tz_name}'.")
        now = datetime.now()
        now_tz_time = now.astimezone(tz_obj)
        html = f"<h1>Current Time in {tz_name}: {now_tz_time.strftime('%Y-%m-%d %H:%M:%S %z')}</h1>"
        status = '200 OK'
        headers = [('Content-Type', 'text/html')]
        start_response(status, headers)
        return [html.encode('utf-8')]
    except Exception as e:
        # Handle errors
        status = '400 Bad Request'
        headers = [('Content-Type', 'text/plain')]
        start_response(status, headers)
        return [f"Error: {str(e)}\n".encode('utf-8')]

# Handle POST /api/v1/time
def handle_post_time(environ, start_response):
    # Returns the current time in the specified timezone as JSON.

    try:
        request_body = environ['wsgi.input'].read(int(environ.get('CONTENT_LENGTH', 0))).decode('utf-8')
        params = json.loads(request_body) if request_body else {}
        tz_name = params.get('tz', None)
        tz_obj = tz.gettz(tz_name) if tz_name else tz.gettz()
        now = datetime.now().astimezone(tz_obj)
        response = {
            "time": now.strftime('%Y-%m-%d %H:%M:%S'),
            "tz": tz_name if tz_name else "Server Time"
        }
        status = '200 OK'
        headers = [('Content-Type', 'application/json')]
        start_response(status, headers)
        return [json.dumps(response).encode('utf-8')]
    except Exception as e:
        # Handle errors
        status = '400 Bad Request'
        headers = [('Content-Type', 'text/plain')]
        start_response(status, headers)
        return [f"Error: {str(e)}\n".encode('utf-8')]

# Handle POST /api/v1/date
def handle_post_date(environ, start_response):
    # Returns the current date in the specified timezone as JSON.
    try:
        request_body = environ['wsgi.input'].read(int(environ.get('CONTENT_LENGTH', 0))).decode('utf-8')
        params = json.loads(request_body) if request_body else {}
        tz_name = params.get('tz', None)
        tz_obj = tz.gettz(tz_name) if tz_name else tz.gettz()
        now = datetime.now().astimezone(tz_obj)
        response = {
            "date": now.strftime('%Y-%m-%d'),
            "tz": tz_name if tz_name else "Server Time"
        }
        status = '200 OK'
        headers = [('Content-Type', 'application/json')]
        start_response(status, headers)
        return [json.dumps(response).encode('utf-8')]
    except Exception as e:
        # Handle errors
        status = '400 Bad Request'
        headers = [('Content-Type', 'text/plain')]
        start_response(status, headers)
        return [f"Error: {str(e)}\n".encode('utf-8')]

# Handle POST /api/v1/datediff
def handle_post_datediff(environ, start_response):
    # Returns the time difference between two dates as JSON.
    try:
        request_body = environ['wsgi.input'].read(int(environ.get('CONTENT_LENGTH', 0))).decode('utf-8')
        params = json.loads(request_body)
        start_date = params['start']['date']
        end_date = params['end']['date']
        start_tz = tz.gettz(params['start'].get('tz', None))
        end_tz = tz.gettz(params['end'].get('tz', None))
        start_dt = datetime.strptime(start_date, '%m.%d.%Y %H:%M:%S').astimezone(start_tz)
        end_dt = datetime.strptime(end_date, '%m.%d.%Y %H:%M:%S').astimezone(end_tz)
        diff = end_dt - start_dt
        response = {"difference": str(diff)}
        status = '200 OK'
        headers = [('Content-Type', 'application/json')]
        start_response(status, headers)
        return [json.dumps(response).encode('utf-8')]
    except Exception as e:
        # Handle errors
        status = '400 Bad Request'
        headers = [('Content-Type', 'text/plain')]
        start_response(status, headers)
        return [f"Error: {str(e)}\n".encode('utf-8')]

# Run the server
if __name__ == '__main__':
    with make_server('', 8000, application) as httpd:
        print("Server running at http://127.0.0.1:8000/")
        httpd.serve_forever()