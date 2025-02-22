import ast
import os
import networkx as nx
import plotly.graph_objects as go
import webbrowser
from pathlib import Path

def expand_user_path(path):
    return os.path.expanduser(path)
  
def parse_imports(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            tree = ast.parse(file.read())
        
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module if node.module else ''
                for alias in node.names:
                    imports.append(f"{module}.{alias.name}")
        return imports
    except Exception as e:
        print(f"Error parsing {file_path}: {str(e)}")
        return []

def generate_import_graph(directory):
    graph = nx.DiGraph()
    file_count = 0
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                module_name = os.path.relpath(file_path, directory).replace('.py', '').replace(os.path.sep, '.')
                
                imports = parse_imports(file_path)
                graph.add_node(module_name)
                
                for imp in imports:
                    if imp.startswith('.'):
                        # Handle relative imports
                        parts = module_name.split('.')
                        imp = '.'.join(parts[:-1]) + imp
                    graph.add_edge(module_name, imp)
                file_count += 1
    
    print(f"Total Python files processed: {file_count}")
    print(f"Number of nodes in graph: {len(graph.nodes)}")
    print(f"Number of edges in graph: {len(graph.edges)}")
    return graph

def visualize_graph_interactive(graph):
    if len(graph.nodes) == 0:
        print("Error: The graph is empty. No visualization can be generated.")
        return

    pos = nx.spring_layout(graph, k=0.5, iterations=50)

    edge_x = []
    edge_y = []
    for edge in graph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in graph.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                # titleside='right'
            ),
            line_width=2))

    node_adjacencies = []
    node_text = []
    for node in graph.nodes():
        adjacencies = list(graph.adj[node])
        node_adjacencies.append(len(adjacencies))
        node_text.append(f'{node}<br># of connections: {len(adjacencies)}')

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Python Project Import Graph',
                        # titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        annotations=[dict(
                            text="",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002)],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )

    # Create HTML file with custom search functionality
    html_string = '''
    <html>
        <head>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.6/d3.min.js"></script>
        </head>
        <body>
            <div>
                <input type="text" id="searchBox" placeholder="Search for a module...">
                <button onclick="searchNode()">Search</button>
            </div>
            <div id="myDiv"></div>
            <script>
                var figure = %s;
                Plotly.newPlot('myDiv', figure.data, figure.layout);
                
                function searchNode() {
                    var searchTerm = document.getElementById('searchBox').value.toLowerCase();
                    var update = {
                        'marker.color': [],
                        'marker.size': []
                    };
                    
                    for (var i = 0; i < figure.data[1].text.length; i++) {
                        var nodeText = figure.data[1].text[i].toLowerCase();
                        if (nodeText.includes(searchTerm)) {
                            update['marker.color'][i] = 'red';
                            update['marker.size'][i] = 20;
                        } else {
                            update['marker.color'][i] = figure.data[1].marker.color[i];
                            update['marker.size'][i] = 10;
                        }
                    }
                    
                    Plotly.restyle('myDiv', update, [1]);
                }
            </script>
        </body>
    </html>
    ''' % fig.to_json()

    with open("import_graph_interactive.html", "w") as f:
        f.write(html_string)
    
    print("Interactive graph saved as 'import_graph_interactive.html'")
    return Path("import_graph_interactive.html").absolute()

def main():
    directory = input("Enter the path to your Python project directory: ")
    print(f"You entered: {directory}")
    
    expanded_directory = expand_user_path(directory)
    print(f"Expanded path: {expanded_directory}")
    
    if not os.path.exists(expanded_directory):
        print(f"Error: The path '{expanded_directory}' does not exist.")
        return
    
    if not os.path.isdir(expanded_directory):
        print(f"Error: '{expanded_directory}' is not a directory.")
        return
    
    try:
        print("Generating import graph...")
        graph = generate_import_graph(expanded_directory)
        
        if len(graph.nodes) > 0:
            print("Visualizing the graph...")
            html_path = visualize_graph_interactive(graph)
            print(f"Opening graph visualization in your default web browser...")
            webbrowser.open(f'file://{html_path}')
        else:
            print("No Python files were found or processed successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()


