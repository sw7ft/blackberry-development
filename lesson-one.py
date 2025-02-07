# Basic Hello World App
from http.server import HTTPServer, BaseHTTPRequestHandler
# import HTTPServer to create a a basic web server an d to define how to handle requests.

def simple_response(handler):
# define a function to handle responses to requests

	if handler.path == "/": 
		# check if the requested web path is web root or in this "/"
		handler.send_response(200)
		# send a HTTP 200 ok response code 
		
		handler.send_header("Content-Type","text/plain")
		
		handler.end_headers()
		
		handler.wfile.write(b"Hello Blackberry World")
	
	else:
		
		handler.send_response(404)
		
		handler.end_headers()
		
		handler.wfile.write(b"Not Found")
	

class SimpleHandler(BaseHTTPRequestHandler):
	# define a request handler class to process HTTP requests
	
	def do_GET(self):
		
		simple_response(self)
		# call our simple_response function to handle the request and send a response
HTTPServer(("",8002), SimpleHandler).serve_forever()

# create a instance of the HTTPServer
# the first argument "" binds the server to all available network interfaces
# the second argument specifies the request handler class (SimpleHandler)
		
