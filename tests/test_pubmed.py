import pytest
from tools.pubmed import PubMedTool

def test_pubmed_fetch_structure():
    tool = PubMedTool()
    query = "Metformin"
    results = tool.search_and_fetch(query, max_results=2)
    
    assert isinstance(results, list)
    if len(results) > 0:
        # التعديل هنا: نتأكد أن العنصر عبارة عن نص وليس قاموس
        assert isinstance(results[0], str) 
        assert len(results[0]) > 20 # التأكد أن النص يحتوي على محتوى فعلي