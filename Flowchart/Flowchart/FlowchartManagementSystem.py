from typing import Dict, List, Set
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from uuid import uuid4, UUID  # Corrected import
import uvicorn

class Node(BaseModel):
    id: str
    label: str = ""

class Edge(BaseModel):
    source: str
    target: str

class Flowchart(BaseModel):
    id: UUID = Field(default_factory=uuid4)  # Corrected to UUID
    nodes: List[Node]
    edges: List[Edge]

    @validator('edges')
    def validate_graph(cls, edges, values):
        # Ensure all nodes in edges exist in the flowchart
        if 'nodes' in values:
            node_ids = {node.id for node in values['nodes']}
            for edge in edges:
                if edge.source not in node_ids or edge.target not in node_ids:
                    raise ValueError("Edge references non-existent nodes")
        return edges

class FlowchartManager:
    def __init__(self):
        self.flowcharts: Dict[UUID, Flowchart] = {}

    def create_flowchart(self, flowchart: Flowchart) -> UUID:
        self.flowcharts[flowchart.id] = flowchart
        return flowchart.id

    def get_flowchart(self, flowchart_id: UUID) -> Flowchart:
        if flowchart_id not in self.flowcharts:
            raise HTTPException(status_code=404, detail="Flowchart not found")
        return self.flowcharts[flowchart_id]

    def update_flowchart(self, flowchart_id: UUID, updated_flowchart: Flowchart) -> Flowchart:
        if flowchart_id not in self.flowcharts:
            raise HTTPException(status_code=404, detail="Flowchart not found")
        
        # Ensure the ID remains the same
        updated_flowchart.id = flowchart_id
        self.flowcharts[flowchart_id] = updated_flowchart
        return updated_flowchart

    def delete_flowchart(self, flowchart_id: UUID):
        if flowchart_id not in self.flowcharts:
            raise HTTPException(status_code=404, detail="Flowchart not found")
        del self.flowcharts[flowchart_id]

    def get_outgoing_edges(self, flowchart_id: UUID, node_id: str) -> List[Edge]:
        flowchart = self.get_flowchart(flowchart_id)
        return [edge for edge in flowchart.edges if edge.source == node_id]

    def get_connected_nodes(self, flowchart_id: UUID, node_id: str) -> Set[str]:
        flowchart = self.get_flowchart(flowchart_id)
        
        # Perform depth-first search to find all connected nodes
        connected = set()
        visited = set()

        def dfs(current_node):
            if current_node in visited:
                return
            visited.add(current_node)
            connected.add(current_node)

            # Find all edges from this node
            for edge in flowchart.edges:
                if edge.source == current_node and edge.target not in visited:
                    dfs(edge.target)
                elif edge.target == current_node and edge.source not in visited:
                    dfs(edge.source)

        dfs(node_id)
        return connected

# FastAPI Application
app = FastAPI(title="Flowchart Management System", 
              description="A system for managing flowcharts with graph operations")

# Initialize flowchart manager
manager = FlowchartManager()

# API Endpoints
@app.post("/flowcharts/", response_model=UUID)
def create_flowchart(flowchart: Flowchart):
    """
    Create a new flowchart
    - Validates graph structure
    - Returns unique flowchart ID
    """
    return manager.create_flowchart(flowchart)

@app.get("/flowcharts/{flowchart_id}", response_model=Flowchart)
def get_flowchart(flowchart_id: UUID):
    """
    Fetch a flowchart by its ID
    """
    return manager.get_flowchart(flowchart_id)

@app.put("/flowcharts/{flowchart_id}", response_model=Flowchart)
def update_flowchart(flowchart_id: UUID, updated_flowchart: Flowchart):
    """
    Update an existing flowchart
    - Preserves original flowchart ID
    - Validates graph structure
    """
    return manager.update_flowchart(flowchart_id, updated_flowchart)

@app.delete("/flowcharts/{flowchart_id}")
def delete_flowchart(flowchart_id: UUID):
    """
    Delete a flowchart by its ID
    """
    manager.delete_flowchart(flowchart_id)
    return {"message": "Flowchart deleted successfully"}

@app.get("/flowcharts/{flowchart_id}/nodes/{node_id}/outgoing-edges")
def get_outgoing_edges(flowchart_id: UUID, node_id: str):
    """
    Get all outgoing edges for a specific node in a flowchart
    """
    return manager.get_outgoing_edges(flowchart_id, node_id)

@app.get("/flowcharts/{flowchart_id}/nodes/{node_id}/connected-nodes")
def get_connected_nodes(flowchart_id: UUID, node_id: str):
    """
    Get all nodes connected to a specific node (directly or indirectly)
    """
    return list(manager.get_connected_nodes(flowchart_id, node_id))

# Standalone running for testing
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
