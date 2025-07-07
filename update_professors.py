import json
import requests
import os

SERPAPI_KEY = os.environ.get("SERPAPI_KEY")

# Load current data
with open("professors.json", "r") as file:
    data = json.load(file)

# Update data using SerpAPI
def fetch_scholar_data(scholar_id):
    if not scholar_id:
        return {"citations": "N/A", "publications": "N/A"}
    
    url = f"https://serpapi.com/search.json?engine=google_scholar_author&author_id={scholar_id}&api_key={SERPAPI_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        result = response.json()
        profile = result.get("author", {})
        stats = result.get("cited_by", {}).get("table", [{}])[0].get("citations", ["0", "0"])
        total_citations = stats[0] if stats else "0"
        total_publications = profile.get("public_access_link_count", 0)
        return {
            "citations": int(total_citations),
            "publications": int(total_publications)
        }
    else:
        return {"citations": "N/A", "publications": "N/A"}

# Update each professor
for prof in data:
    if prof["scholar_url"]:
        scholar_id = prof["scholar_url"].split("user=")[-1].split("&")[0]
        stats = fetch_scholar_data(scholar_id)
        prof["citations"] = stats["citations"]
        prof["publications"] = stats["publications"]

# Save updated data
with open("professors.json", "w") as file:
    json.dump(data, file, indent=4)

print("✅ Professors data updated.")
