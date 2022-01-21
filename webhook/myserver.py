from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
import sys
from io import BytesIO
from pathlib import Path

KEY_DIR = Path.cwd() / '.pem'
class MyHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        print(body)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())

if len(sys.argv) < 2:
    print("usage: {} <ip address of the local host>".format(sys.argv[0]))

host_ip = sys.argv[1]
# run this on cnfdd4 10.19.17.161
httpd = HTTPServer((host_ip, 4443), MyHTTPRequestHandler)

# copy *.pem to current directory
httpd.socket = ssl.wrap_socket (httpd.socket, 
        keyfile=KEY_DIR / "key.pem", 
        certfile=KEY_DIR / 'cert.pem', server_side=True)

httpd.serve_forever()
