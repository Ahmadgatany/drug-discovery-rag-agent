from Bio import Entrez
from core.config import Config

class PubMedTool:
    def __init__(self):
        Entrez.email = Config.ENTREZ_EMAIL

    def search_and_fetch(self, query, max_results=5):
        try:
            # 1. البحث عن IDs للأبحاث
            handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
            record = Entrez.read(handle)
            handle.close()
            id_list = record["IdList"]

            if not id_list:
                return []

            # 2. جلب تفاصيل الأبحاث (العناوين والملخصات)
            handle = Entrez.efetch(db="pubmed", id=",".join(id_list), rettype="medline", retmode="text")
            lines = handle.readlines()
            handle.close()

            # معالجة بسيطة للنصوص المستخرجة
            results = []
            current_article = ""
            for line in lines:
                if line.startswith("TI  -"): # العنوان
                    current_article += line[5:].strip() + " "
                if line.startswith("AB  -"): # الملخص
                    current_article += line[5:].strip() + " "
                if line.startswith("PMID-"): # نهاية البحث الحالي
                    if current_article:
                        results.append(current_article)
                        current_article = ""
            
            return results
        except Exception as e:
            print(f"Error fetching from PubMed: {e}")
            return []