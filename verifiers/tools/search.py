def search_ddg(query: str, num_results: int = 5) -> str:
    """Searches DuckDuckGo and returns concise summaries of top results.
    
    Args:
        query: The search query string
        num_results: Number of results to return (default: 5, max: 10)
        
    Returns:
        Formatted string with bullet points of top results, each with title and brief summary
        
    Examples:
        {"query": "who invented the lightbulb", "num_results": 3}
    """
    from duckduckgo_search import DDGS

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=min(num_results, 10)))
            if not results:
                return "No results found"

            summaries = []
            for r in results:
                title = r['title']
                snippet = r['body'][:200].rsplit('.', 1)[0] + '.'
                summaries.append(f"• {title}\n  {snippet}")

            return "\n\n".join(summaries)
    except Exception as e:
        return f"Error: {str(e)}" 
    
def search_brave(query: str, num_results: int = 5) -> str:
    """Searches Brave and returns concise summaries of top results.
    
    Args:
        query: The search query string
        num_results: Number of results to return (default: 5, max: 10)
        
    Returns:
        Formatted string with bullet points of top results, each with title, source, and brief summary
        
    Examples:
        {"query": "who invented the lightbulb", "num_results": 3}
    """
    from brave import Brave
    from typing import List, Dict, Any

    try:
        brave = Brave()
        results = brave.search(q=query, count=min(num_results, 10)) # type: ignore
        results: List[Dict[str, Any]] = results.web_results # type: ignore
        
        if not results:
            return "No results found"

        summaries = []
        for r in results:
            header = f"{r['profile']['name']} ({r['profile']['long_name']})"
            title = r['title']
            snippet = r['description'] #[:200].rsplit('.', 1)[0] + '.'
            summaries.append(f"•  {header}\n   {title}\n   {snippet}")

        return "\n\n".join(summaries)
    except Exception as e:
        return f"Error: {str(e)}"

def search_RAG(query: str, num_results: int = 5) -> str:
    """
    Searches the local RAG retriever server and returns concise summaries of top results.
    
    Args:
        query: The search query string
        num_results: Number of results to return (default: 5)
        
    Returns:
        Formatted string with bullet points of top results, each with title and brief summary.
        
    Examples:
        {"query": "what is artificial intelligence", "num_results": 3}
    """
    import requests

    try:
        url = "http://127.0.0.1:8000/retrieve"
        payload = {"queries": [query], "topk": num_results, "return_scores": False}
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            return f"Error: {response.status_code}"
        data = response.json()
        results = data.get("result", [])
        if not results or not results[0]:
            return "No results found"
        
        summaries = []
        for doc in results[0]:
            title = doc.get("title", "No Title")
            text = doc.get("text", "No text available")
            # Create a snippet by taking the first 200 characters and ending at the last period if possible.
            snippet = text[:200]
            if '.' in snippet:
                snippet = snippet.rsplit('.', 1)[0] + '.'
            summaries.append(f"• {title}\n  {snippet}")
        return "\n\n".join(summaries)
    except Exception as e:
        return f"Error: {str(e)}"
