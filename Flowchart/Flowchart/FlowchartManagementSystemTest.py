import pytest
from fastapi.testclient import TestClient
from FlowchartManagementSystem import app, Node, Edge, Flowchart

client = TestClient(app)

@pytest.fixture
def sample_flowchart():
    return Flowchart(
        nodes=[
            Node(id="node1", label="Start"),
            Node(id="node2", label="Process"),
            Node(id="node3", label="End")
        ],
        edges=[
            Edge(source="node1", target="node2"),
            Edge(source="node2", target="node3")
        ]
    )

def test_create_flowchart(sample_flowchart):
    response = client.post("/flowcharts/", json=sample_flowchart.dict())
    assert response.status_code == 200
    flowchart_id = response.json()
    
    # Fetch the created flowchart
    fetch_response = client.get(f"/flowcharts/{flowchart_id}")
    assert fetch_response.status_code == 200
    assert fetch_response.json()['nodes'] == sample_flowchart.dict()['nodes']
    assert fetch_response.json()['edges'] == sample_flowchart.dict()['edges']

def test_invalid_flowchart_creation():
    invalid_flowchart = {
        "nodes": [{"id": "node1"}],
        "edges": [{"source": "node2", "target": "node3"}]  # References non-existent nodes
    }
    response = client.post("/flowcharts/", json=invalid_flowchart)
    assert response.status_code == 422  # Validation error

def test_update_flowchart(sample_flowchart):
    # First create a flowchart
    create_response = client.post("/flowcharts/", json=sample_flowchart.dict())
    flowchart_id = create_response.json()
    
    # Update the flowchart
    updated_flowchart = Flowchart(
        nodes=[
            Node(id="node1", label="Start"),
            Node(id="node2", label="Process"),
            Node(id="node3", label="End"),
            Node(id="node4", label="New Node")
        ],
        edges=[
            Edge(source="node1", target="node2"),
            Edge(source="node2", target="node3"),]
    )