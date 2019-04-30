from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

## import CRUD Operations from Lession 1 ##
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith("/restaurants"):
				restaurants = session.query(Restaurant).all()
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1>List of Restaurants</h1>"
				for restaurant in restaurants:
					output += restaurant.name
					output += "</br>"
					output += "<a href ='/edit'>Edit</a> &ensp;"
					output += "<a href =" ">Delete</a>"
					output += "</br></br>"
					output += "</body></html>"
				self.wfile.write(output)
				return

			if self.path.endswith("/edit"):
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1>What do you want to edit?</h1>"
				output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants'><h4>current name</h4><input name="curname" type="text" ></br><h4>new name</h4><input name="newname" type="text"><input type="submit" value="Submit"></form>'''
				output += "</body><html>"
				self.wfile.write(output)
				return

			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1>Hello!</h1>"
				output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"></form>'''
				output += "</body></html>"
				#wfile: Contains the output stream for writing a response back to the client
				self.wfile.write(output) #display the actual html on the web browser
				#this will print the html to the terminal
				#print (output)
				return

			if self.path.endswith("/hola"):
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<h1>Hola!</h1>"
				#the value of the action attribute will change the end of the URL.
				output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"></form>'''
				output += "</body></html>"
				self.wfile.write(output)
				print (output)
				return

		except IOerror:
			self.send_error(404,"File Not Found %s" % self.path)	


	def do_POST(self):
		try:
			self.send_response(301)
			self.send_header('Content-type','text/html')
			self.end_headers()
			ctype, pdict = cgi.parse_header(
				self.headers.getheader('content-type'))
			#rfile contains an input stream
			if ctype == 'multipart/form-data':
				fields = cgi.parse_multipart(self.rfile, pdict)
				CurrentName = fields['curname'][0]
				NewName = fields['newname'][0]
				restaurants = session.query(Restaurant).filter_by(name = CurrentName)
				for restaurant in restaurants:
					if restaurant.name == CurrentName:
						matchedID = restaurant.ID
				restaurant.name = NewName
				session.add(restaurant)
				session.commit()
				restaurants = session.query(Restaurant).all()		
			output = ""
			output += "<html><body>"
			output += "<h1>List of Restaurants</h1>"
			for restaurant in restaurants:
				output += restaurant.name
				output += "</br>"
				output += "<a href ='/edit'>Edit</a> &ensp;"
				output += "<a href =" ">Delete</a>"
				output += "</br></br>"
				output += "</body></html>"
			self.wfile.write(output)

		except:
			pass

def main():
	try: 
		port = 8080
		server = HTTPServer(('',port), webserverHandler)
		print ("Web server running on port %s" % port)
		server.serve_forever()

	except KeyboardInterrupt:
		print (" stopping web server...")
		server.socket.close()

if __name__ == "__main__":
	main()