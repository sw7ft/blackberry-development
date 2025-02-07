import sqlite3 # this imports the native sqlite3 library
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

DB_FILE = "data.db"

# Create Database and Create Table

def init_db():
	conn = sqlite3.connect(DB_FILE)
	cursor = conn.cursor()
	cursor.execute("""
        CREATE TABLE IF NOT EXISTS entries (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT NOT NULL,
			message TEXT NOT NULL
		)
	""")
	conn.commit()
	conn.close()
	
class SimpleFormHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path == "/":
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()
			
			# CRUD - READ Operation

			conn = sqlite3.connect(DB_FILE)
			cursor = conn.cursor()
			cursor.execute("SELECT name, message from entries")
			rows = cursor.fetchall()
			conn.close()
			
			html_content = """<!DOCTYPE html>
			<html>
			<head><title>Simple Form</title></head>
			<body>
				<h2>Submit Entrie</h2>
				<form method=post>
					Name: <input type=text name=name><br><br>
					Message: <textarea name=message></textarea>
					<input type=submit value=submit>
				</form>
				<h2>Stored Entries</h2>
				<ul>""" + "".join(f"<li><b>{name}:</b> {message}</li>" for name,message in rows) + """
				</ul>
			</body>
			</html>"""
			
			self.wfile.write(html_content.encode("utf-8"))
			
	def do_POST(self):
		content_length = int(self.headers["Content-Length"])
		post_data = self.rfile.read(content_length)
		params = urllib.parse.parse_qs(post_data.decode("utf-8"))
		
		name = params.get("name",[""])[0]
		message = params.get("message",[""])[0]
		
		if name and message:
			conn = sqlite3.connect(DB_FILE)
			cursor = conn.cursor()
			cursor.execute("INSERT INTO entries (name,message) VALUES (?,?)",(name,message))
			conn.commit()
			conn.close()
		# redirect
		self.send_response(303)
		self.send_header("Location","/")
		self.end_headers()
		

if __name__ == "__main__":
	init_db()
	server_address = ("",8005)
	httpd = HTTPServer(server_address,SimpleFormHandler)
	print("server running at localhost port 8005")
	httpd.serve_forever()
