# Python Import Graph Generator
This script generates an interactive visualization of import relationships in a Python project. It helps you understand how different modules in your project are connected through imports.

## What it does
1. Scans a specified Python project directory.
2. Analyzes all Python files to find import statements.
3. Creates a graph where:
   - Nodes represent Python modules
   - Edges represent import relationships
4. Generates an interactive HTML visualization of this graph.
5. Opens the visualization in your default web browser.
6. Allows users to download the generated PNG image of the plot.

## How to use it
1. Make sure you have Python installed on your system.
2. Install the required libraries:
   ```
   pip install networkx plotly
   ```
3. Run the script:
   ```
   python main.py
   ```
4. When prompted, enter the path to your Python project directory.
5. The script will process your project and automatically open a web browser with the visualization.

## Interacting with the visualization
- Hover over nodes to see module names and the number of connections.
- Use the search box to find specific modules:
  1. Type part of a module name in the search box.
  2. Click the "Search" button.
  3. Matching nodes will be highlighted in red and enlarged.
- Zoom in/out and pan around the graph using your mouse or touchpad.

## Troubleshooting
- If the browser doesn't open automatically, look for a file named `import_graph_interactive.html` in the same directory as the script and open it manually.
- Make sure you have permission to read the Python files in your project directory.
- For large projects, the graph may take a moment to generate and render.

## Limitations
- The script only analyzes static imports and may not capture dynamic imports or complex import patterns.
- Very large projects may result in cluttered graphs that are difficult to navigate.
