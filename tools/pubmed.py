from Bio import Entrez
from core.config import Config

class PubMedTool:
    def __init__(self):
        Entrez.email = Config.ENTREZ_EMAIL

    def search_and_fetch(self, query, max_results=5):
        try:
            handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
            record = Entrez.read(handle)
            handle.close()
            id_list = record["IdList"]

            if not id_list:
                return []

            handle = Entrez.efetch(db="pubmed", id=",".join(id_list), rettype="medline", retmode="text")
            lines = handle.readlines()
            handle.close()

            results = []
            current_article = ""
            for line in lines:
                if line.startswith("TI  -"): 
                    current_article += line[5:].strip() + " "
                if line.startswith("AB  -"): 
                    current_article += line[5:].strip() + " "
                if line.startswith("PMID-"): 
                    if current_article:
                        results.append(current_article)
                        current_article = ""
            
            return results
        except Exception as e:
            print(f"Error fetching from PubMed: {e}")
            return []