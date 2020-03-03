

class Collaborator:
	def __init__(self, id, connections, interests, name="UNKNOWN"):
		self.name = name
		self.id = id
		self.connections = connections
		self.interests = interests
	def __repr__(self):
		return "Researcher: {}; ID: {}; Interests: {}; Connections: {}".format(self.name, self.id, self.interests, self.connections)
	def add_connection(self, id):
		if id not in self.connections.keys():
			self.connections[id] = 1
		else:
			self.connections[id] += 1

def main():
	#network = collect_network()
	network = read_network()
	generate_csv_network(network)
	#output_network(network)
	#display_network(network)
	#print(network["Chris Lupo"])

def generate_csv_network(network):
	import csv
	with open('network.csv', 'w', newline='', encoding='utf-8') as csvfile:
		fieldnames = ['subject', 'type', 'target']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		for researcher in network.keys():
			for connection in network[researcher].connections.keys():
				collaborations = network[researcher].connections[connection]
				connectionStrength = ""
				if collaborations == 1:
					connectionStrength = "WEAKLY_CONNECTED"
				elif collaborations < 5:
					connectionStrength = "NORMALLY_CONNECTED"
				else:
					connectionStrength = "STRONGLY_CONNECTED"
				writer.writerow({'subject': researcher, 'type': connectionStrength, 'target': connection})
			for interest in network[researcher].interests:
				writer.writerow({'subject': researcher, 'type': 'INTERESTED_IN', 'target': interest})

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
		network[attributes[1]] = Collaborator(int(attributes[0]), ast.literal_eval(attributes[3]), ast.literal_eval(attributes[2]), attributes[1])
	f.close()
	return network
	
#output a given network to a textfile
def output_network(network):
	f = open("network.txt","w+")
	for key in sorted(network):
		collaborator = network[key]
		f.write("{}| {}| {}| {}\n".format(collaborator.id, collaborator.name, collaborator.interests, collaborator.connections))
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
		authorNames = []
		for author in authorsQueryResults:
			query = "SELECT name FROM cpcollabnet2019.Researcher WHERE rid = " + str(author[0])
			cursor.execute(query)
			nameQueryResults = cursor.fetchall()
			if len(nameQueryResults) != 0:
				if nameQueryResults[0][0] not in network.keys():
					interests = []
					query = "SELECT interest FROM cpcollabnet2019.Interest WHERE rid = " + str(author[0])
					cursor.execute(query)
					interestQueryResults = cursor.fetchall()
					for interest in interestQueryResults:
						interests.append(interest[0])
					network[nameQueryResults[0][0]] = Collaborator(author[0], {}, interests, nameQueryResults[0][0])
				authorNames.append(nameQueryResults[0][0])
				
		#add connections between all the authors that worked on the paper
		for i in range(len(authorNames) - 1):
			for j in range(i + 1, len(authorNames)):
				network[authorNames[i]].add_connection(authorNames[j])
				network[authorNames[j]].add_connection(authorNames[i])
				
	cursor.close()
	cnx.close()
	return network
	

   
if __name__=="__main__":
	main()

