from app import create_app

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='0.0.0.0', 
    help='Host name')
    parser.add_argument('-p', '--port', default=8888, help='Port number')
    args = parser.parse_args()

    app = create_app()    
    app.run(host=args.host, port=args.port)

