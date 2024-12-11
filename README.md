# Flowchart Management System

## Overview

This system allows users to manage flowcharts represented as directed graphs. A flowchart consists of nodes and edges, and users can create, read, update, and delete flowcharts. Additionally, the system supports graph validation and allows querying of outgoing edges and connected nodes.
This will start the FastAPI server, and the application will be available at http://127.0.0.1:8000.

## API Endpoints
Here are the available API endpoints for managing flowcharts:
1. Create Flowchart
URL: /flowcharts/
Method: POST
Description: Create a new flowchart.
Request Body: JSON object containing nodes and edges.
Response: Flowchart ID (UUID).
2. Fetch Flowchart by ID
URL: /flowcharts/{flowchart_id}
Method: GET
Description: Fetch details of a flowchart by its ID.
Response: Flowchart object containing nodes and edges.
3. Update Flowchart
URL: /flowcharts/{flowchart_id}
Method: PUT
Description: Update an existing flowchart.
Request Body: JSON object containing updated nodes and edges.
Response: Updated flowchart object.
4. Delete Flowchart
URL: /flowcharts/{flowchart_id}
Method: DELETE
Description: Delete a flowchart by its ID.
Response: Success message.
5. Get Outgoing Edges for a Node
URL: /flowcharts/{flowchart_id}/nodes/{node_id}/outgoing-edges
Method: GET
Description: Get all outgoing edges from a specific node in the flowchart.
Response: List of edges originating from the specified node.
6. Get Connected Nodes
URL: /flowcharts/{flowchart_id}/nodes/{node_id}/connected-nodes
Method: GET
Description: Get all nodes connected to a specific node (directly or indirectly).
Response: List of node IDs connected to the specified node.
