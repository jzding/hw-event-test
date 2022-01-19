from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
from io import BytesIO

class MyHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())

# run this on cnfdd4 10.19.17.161
httpd = HTTPServer(('10.19.17.161', 4443), MyHTTPRequestHandler)

# copy *.pem to current directory
httpd.socket = ssl.wrap_socket (httpd.socket, 
        keyfile="key.pem", 
        certfile='cert.pem', server_side=True)

httpd.serve_forever()
