

class Collaborator:
	def __init__(self, id, connections, name="UNKNOWN"):
		self.name = name
		self.id = id
		self.connections = connections
	def __repr__(self):
		return "Researcher: {}; ID: {}; Connections: {}".format(self.name, self.id, self.connections)
	def add_connection(self, id):
		if id not in self.connections.keys():
			self.connections[id] = 1
		else:
			self.connections[id] += 1

def main():
	#network = collect_network()
	network = read_network()
	#output_network(network)
	#display_network(network)
	print(network[1])

#display the contents of the given network in the console
def display_network(network):
	for key in sorted(network):
		print(network[key])

#create a network by reading in from a textfile
def read_network():
	import ast
	network = {}
	f = open("network.txt", "r")
	collaborators = f.readlines()
	for collaborator in collaborators:
		attributes = collaborator.split("| ") #each line is formatted: <id>| <name>| <dictionary of connections>
		network[int(attributes[0])] = Collaborator(int(attributes[0]), ast.literal_eval(attributes[2]), attributes[1])
	f.close()
	return network
	
#output a given network to a textfile
def output_network(network):
	f = open("network.txt","w+")
	for key in sorted(network):
		collaborator = network[key]
		f.write("{}| {}| {}\n".format(collaborator.id, collaborator.name, collaborator.connections))
	f.close()

#create a network from the database
def collect_network():
	import mysql.connector
	network = {}
	cnx = mysql.connector.connect(user='kurfess-students', password='haveagoodquart3r', host='cpcollabnetwork8.cn244vkxrxzn.us-west-1.rds.amazonaws.com')
	cursor = cnx.cursor()

	#get the papers that have authors from the Cal Poly CS department
	query = ("SELECT DISTINCT cid FROM cpcollabnet2019.Author WHERE rid IN (SELECT rid FROM cpcollabnet2019.Researcher WHERE rid IN (SELECT rid FROM cpcollabnet2019.Employment WHERE did = 1))")
	cursor.execute(query)
	papersQueryResults = cursor.fetchall() #for each row, index 0 -> cid
	
	for paper in papersQueryResults:
		#get all the authors that worked on the current paper being processed
		query = "SELECT rid FROM cpcollabnet2019.Author WHERE cid = " + str(paper[0])
		cursor.execute(query)
		authorsQueryResults = cursor.fetchall() #for each row, index 0 -> rid
		
		#make sure that all the authors are in the network
		for author in authorsQueryResults:
			if author[0] not in network.keys():
				query = "SELECT name FROM cpcollabnet2019.Researcher WHERE rid = " + str(author[0])
				cursor.execute(query)
				nameQueryResults = cursor.fetchall()
				if len(nameQueryResults) != 0:
					network[author[0]] = Collaborator(author[0], {}, nameQueryResults[0][0])
				else:
					network[author[0]] = Collaborator(author[0], {})
		
		#add connections between all the authors that worked on the paper
		for i in range(len(authorsQueryResults) - 1):
			for j in range(i + 1, len(authorsQueryResults)):
				network[authorsQueryResults[i][0]].add_connection(authorsQueryResults[j][0])
				network[authorsQueryResults[j][0]].add_connection(authorsQueryResults[i][0])
				
	cursor.close()
	cnx.close()
	return network
	

   
if __name__=="__main__":
	main()

