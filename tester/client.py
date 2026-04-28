import requests
import time

def make_request(url, timeout=3, max_retries=1):
    """
    Makes a request to the given URL and returns the response object
    and the latency in milliseconds.
    Includes a timeout and basic retry mechanism.
    """
    for attempt in range(max_retries + 1):
        start_time = time.time()
        try:
            response = requests.get(url, timeout=timeout)
            latency_ms = (time.time() - start_time) * 1000
            
            # If rate limited or 5xx error, retry after a short delay
            if response.status_code == 429 or response.status_code >= 500:
                if attempt < max_retries:
                    time.sleep(1) # Backoff
                    continue
                    
            return response, latency_ms
            
        except requests.exceptions.RequestException as e:
            if attempt < max_retries:
                time.sleep(1) # Backoff
                continue
            latency_ms = (time.time() - start_time) * 1000
            return None, latency_ms
