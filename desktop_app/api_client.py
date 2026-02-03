import json
import os
import requests
from typing import Optional
from config import BASE_API_URL, TOKENS_FILE

class ApiClient:
    def __init__(self, base_url: str = BASE_API_URL):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.tokens_path = os.path.join(os.path.dirname(__file__), TOKENS_FILE)
        self.access = None
        self.refresh = None
        self._load_tokens()

    def _load_tokens(self):
        if os.path.exists(self.tokens_path):
            try:
                data = json.load(open(self.tokens_path, 'r'))
                self.access = data.get('access')
                self.refresh = data.get('refresh')
                if self.access:
                    self.session.headers.update({'Authorization': f'Bearer {self.access}'})
            except Exception:
                pass

    def _save_tokens(self):
        data = {'access': self.access, 'refresh': self.refresh}
        with open(self.tokens_path, 'w') as f:
            json.dump(data, f)

    def clear_tokens(self):
        self.access = None
        self.refresh = None
        try:
            os.remove(self.tokens_path)
        except Exception:
            pass
        self.session.headers.pop('Authorization', None)

    def _refresh_access(self) -> bool:
        if not self.refresh:
            return False
        url = f"{self.base_url}/api/auth/refresh/"
        try:
            r = self.session.post(url, json={'refresh': self.refresh}, timeout=10)
            if r.status_code == 200:
                data = r.json()
                self.access = data.get('access')
                if self.access:
                    self.session.headers.update({'Authorization': f'Bearer {self.access}'})
                    self._save_tokens()
                    return True
        except Exception:
            pass
        return False

    def _request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"
        r = self.session.request(method, url, **kwargs)
        if r.status_code == 401:
            # try refresh once
            if self._refresh_access():
                r = self.session.request(method, url, **kwargs)
        return r

    # Auth
    def login(self, username: str, password: str) -> Optional[dict]:
        url = '/api/auth/login/'
        r = self._request('POST', url, json={'username': username, 'password': password})
        if r.status_code == 200:
            data = r.json()
            self.access = data.get('access')
            self.refresh = data.get('refresh')
            if not self.access and isinstance(data.get('tokens'), dict):
                # older shape
                self.access = data['tokens'].get('access')
                self.refresh = data['tokens'].get('refresh')
            if self.access:
                self.session.headers.update({'Authorization': f'Bearer {self.access}'})
                self._save_tokens()
            return data
        else:
            raise Exception(r.text)

    def signup(self, username: str, email: str, password: str) -> Optional[dict]:
        url = '/api/signup/'
        r = self._request('POST', url, json={'username': username, 'email': email, 'password': password})
        if r.status_code in (200, 201):
            data = r.json()
            # backend returns top-level access/refresh
            self.access = data.get('access') or (data.get('tokens') or {}).get('access')
            self.refresh = data.get('refresh') or (data.get('tokens') or {}).get('refresh')
            if self.access:
                self.session.headers.update({'Authorization': f'Bearer {self.access}'})
                self._save_tokens()
            return data
        else:
            raise Exception(r.text)

    # Datasets
    def upload_csv(self, file_path: str):
        url = '/api/datasets/upload/'
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f, 'text/csv')}
            r = self._request('POST', url, files=files, timeout=60)
            if r.status_code in (200, 201):
                return r.json()
            raise Exception(r.text)

    def list_datasets(self):
        url = '/api/datasets/'
        r = self._request('GET', url)
        if r.status_code == 200:
            return r.json()
        raise Exception(r.text)

    def get_summary(self, dataset_id: str):
        url = f'/api/datasets/{dataset_id}/summary/'
        r = self._request('GET', url)
        if r.status_code == 200:
            return r.json()
        raise Exception(r.text)

    def get_table(self, dataset_id: str, page=1, page_size=200):
        url = f'/api/datasets/{dataset_id}/table/?page={page}&page_size={page_size}'
        r = self._request('GET', url, timeout=30)
        if r.status_code == 200:
            return r.json()
        raise Exception(r.text)

    def download_report(self, dataset_id: str, dest_path: str):
        url = f'/api/datasets/{dataset_id}/report/'
        r = self._request('GET', url, stream=True)
        if r.status_code == 200:
            with open(dest_path, 'wb') as f:
                for chunk in r.iter_content(1024 * 32):
                    f.write(chunk)
            return dest_path
        
        err_msg = r.text[:200]
        raise Exception(f"Failed to download report (HTTP {r.status_code}): {err_msg}")

    def download_clean_csv(self, dataset_id: str, dest_path: str):
        url = f'/api/datasets/{dataset_id}/download_clean/'
        r = self._request('GET', url, stream=True)
        if r.status_code == 200:
            with open(dest_path, 'wb') as f:
                for chunk in r.iter_content(1024 * 32):
                    f.write(chunk)
            return dest_path
        
        err_msg = r.text[:200]
        raise Exception(f"Failed to download data (HTTP {r.status_code}): {err_msg}")
