from tavily import TavilyClient
from core.config import Config

class WebSearchTool:
    def __init__(self):
        if not Config.TAVILY_API_KEY:
            print("[!] Warning: TAVILY_API_KEY not found in Config.")
        self.client = TavilyClient(api_key=Config.TAVILY_API_KEY)

    def search(self, query: str):
        """
        This function searches the web for the latest medical information (2024-2025).
        """
        try:
            search_result = self.client.search(
                query=query,
                search_depth="advanced",
                max_results=3,
                include_answer=False 
            )
            
            formatted_results = []
            for res in search_result.get('results', []):
                title = res.get('title', 'No Title')
                content = res.get('content', 'No Content')
                url = res.get('url', '#')
                formatted_results.append(f"Source: {title}\nContent: {content}\nLink: {url}")
            
            return "\n\n".join(formatted_results) if formatted_results else "No relevant web updates found."
            
        except Exception as e:
            return f"Error during Web Search: {str(e)}"