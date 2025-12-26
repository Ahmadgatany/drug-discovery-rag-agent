import pytest
from core.agent import MedicalAgent
from tools.graph import GraphTool
from tools.vector_db import VectorTool
from tools.web_search import WebSearchTool


# --- اختبار الـ Agent ---
def test_agent_initialization_and_search():
    """اختبار أن العميل الطبي يعمل ويعيد قاموس بيانات"""
    graph = GraphTool()
    vector = VectorTool()
    web = WebSearchTool()
    
    agent = MedicalAgent(graph_tool=graph, vector_tool=vector, web_tool=web)
    
    # تنفيذ البحث (بدون await لأنها دالة عادية)
    response = agent.search("Aspirin")
    
    assert isinstance(response, dict)
    assert "answer" in response

# --- اختبار أداة الجراف (التي أرسلت لي كودها) ---
def test_graph_query_logic():
    """اختبار دالة الـ Cypher داخل أداة الجراف"""
    graph = GraphTool()
    
    # استدعاء الدالة التي كتبتها أنت
    result = graph.query("Aspirin")
    
    assert isinstance(result, str)
    assert "Graph query error" not in result