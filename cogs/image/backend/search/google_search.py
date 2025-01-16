import requests

class GoogleSearchAPI:
    def __init__(self, api_key, cse_id):
        self.api_key = api_key
        self.cse_id = cse_id
        self.base_url = "https://www.googleapis.com/customsearch/v1"
        
    def search(self, query, search_type="searchTypeUndefined", safe_search="active"):
        params = {
            "q": query,
            "cx": self.cse_id,
            "key": self.api_key,
            "searchType": search_type,
            "num": 10,
            "safe": safe_search
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()  # Raise an error for bad status codes
            results = response.json()

            return results
            
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def search_get_image_link_list(self, query, safe_search="active"):
        results = self.search(query, "image", safe_search)

        image_list = []
        if results != None:
            image_list = [item["link"] for item in results.get("items", [])]

        return image_list


    def search_get_image_list(self, query, safe_search="active"):
        results = self.search(query, "image", safe_search)
        image_list = []
        if results != None:
            image_list = results["items"]

        return image_list

if __name__ == "__main__":
    from dotenv import load_dotenv
    import os
    load_dotenv()
    api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
    cse_id = os.getenv("GOOGLE_IMAGE_SEARCH_SS_CSE_ID")
    api = GoogleSearchAPI(api_key, cse_id)
    results = api.search_get_image_list(input("Search Query: "))
    print(results)
