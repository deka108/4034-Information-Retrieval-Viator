from server.server_app import app

import argparse

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='0.0.0.0', 
    help='Host name')
    parser.add_argument('-p', '--port', default=3000, help='Port number')
    args = parser.parse_args() 

    app.run(host=args.host, port=args.port)
