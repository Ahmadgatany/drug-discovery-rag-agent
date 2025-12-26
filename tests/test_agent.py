import pytest
from core.agent import MedicalAgent
from tools.graph import GraphTool
from tools.vector_db import VectorTool
from tools.web_search import WebSearchTool


# --- اختبار الـ Agent ---
def test_agent_initialization_and_search():
    """Test that the medical agent works correctly and returns a data dictionary"""
    graph = GraphTool()
    vector = VectorTool()
    web = WebSearchTool()
    
    agent = MedicalAgent(graph_tool=graph, vector_tool=vector, web_tool=web)
    

    response = agent.search("Aspirin")
    
    assert isinstance(response, dict)
    assert "answer" in response

def test_graph_query_logic():
    graph = GraphTool()
    result = graph.query("Aspirin")
    
    assert isinstance(result, str)
    assert "Graph query error" not in result