import requests

class JobSearcher:
    API_URL = "https://remoteok.com/api"
    HEADERS = {"User-Agent": "Mozilla/5.0"}  # Prevent request blocking

    def fetch_jobs(self):
        try:
            response = requests.get(self.API_URL, headers=self.HEADERS)
            if response.status_code == 200:
                return response.json()
            else:
                return []
        except requests.RequestException as e:
            print(f"Error fetching jobs: {e}")
            return []

    def search_by_keyword(self, keyword: str):
        all_jobs = self.fetch_jobs()
        jobs = all_jobs[1:] if all_jobs and isinstance(all_jobs[0], dict) and 'id' not in all_jobs[0] else all_jobs
        
        keyword = keyword.lower()
        filtered = []
        for job in jobs:
            title = job.get('position', '').lower()
            description = job.get('description', '').lower()
            tags = [tag.lower() for tag in job.get('tags', []) if isinstance(tag, str)]
            company = job.get('company', '').lower()

            if any(keyword in field for field in [title, description, company]) or any(keyword in tag for tag in tags):
                filtered.append(job)

        return filtered

