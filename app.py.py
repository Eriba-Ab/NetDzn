from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure value

network_topology = {}


class Graph:
    def __init__(self):
        self.graph = {}

    def add_node(self, node, connected_nodes, edge_weights):
        if not node:
            raise ValueError('Node name cannot be empty.')
        if node in self.graph:
            raise ValueError('Node already exists.')
        new_node_entry = {dest: weight for dest, weight in zip(connected_nodes, edge_weights)}
        self.graph[node] = new_node_entry

    def dijkstra(self, start, end):
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0
        parents = {}

        while distances:
            current_node = min(distances, key=distances.get)
            for neighbor, cost in self.graph[current_node].items():
                if distances[current_node] + cost < distances[neighbor]:
                    distances[neighbor] = distances[current_node] + cost
                    parents[neighbor] = current_node
            distances.pop(current_node)

        path = []
        while end:
            path.insert(0, end)
            end = parents.get(end)
        return path
"""class Graph:
    def __init__(self):
        self.graph = {}

    def add_node(self, node, connected_nodes, edge_weights):
        new_node_entry = {dest: weight for dest, weight in zip(connected_nodes, edge_weights)}
        self.graph[node] = new_node_entry

    def dijkstra(self, start, end):
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0
        parents = {}
        visited = set()

        while distances:
            current_node = min(distances, key=distances.get)
            for neighbor, cost in self.graph[current_node].items():
                if distances[current_node] + cost < distances[neighbor]:
                    distances[neighbor] = distances[current_node] + cost
                    parents[neighbor] = current_node
            visited.add(current_node)
            distances.pop(current_node)

        path = []
        while end:
            path.insert(0, end)
            end = parents.get(end)
        return path, distances[path[0]]
"""
# Create an instance of the Graph class to manage the network topology.
graph = Graph()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            new_node = request.form['node'].strip()
            connected_nodes = request.form['edge'].split(',')
            edge_weights = request.form['weight'].split(',')  # Split without converting to integers

            if not new_node:
                raise ValueError('Node name cannot be empty.')

            if not connected_nodes or not edge_weights:
                # This is the last node, so provide default values for connected nodes and edge weights
                connected_nodes = []
                edge_weights = []

            # Convert edge weights to integers, skipping empty strings
            edge_weights = [int(weight) if weight.strip() else 0 for weight in edge_weights]

            # Add the new node and its connections to the network topology.
            graph.add_node(new_node, connected_nodes, edge_weights)

            flash(f'Node {new_node} added successfully.', 'success')
        except ValueError as e:
            flash(f'Error: {str(e)}', 'error')

    return render_template('index.html', last_node=False)

@app.route('/Done', methods=['POST'])
def Done():
         if request.method == 'POST':
          return render_template('result.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    source = request.form['source']
    destination = request.form['destination']

    if source not in graph.graph or destination not in graph.graph:
        flash('Invalid source or destination node.')
        return redirect(url_for('index'))

    # Calculate the shortest path and cost using Dijkstra's algorithm.
    shortest_path, cost = graph.dijkstra(source, destination)
    return render_template('result.html', path=shortest_path, cost=cost)

if __name__ == '__main__':
    app.run(debug=True)
