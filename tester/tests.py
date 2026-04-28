from .client import make_request
import time

def run_tests():
    base_url = "https://api.agify.io"
    results = []
    
    # Test 1: Valid name
    url = f"{base_url}?name=michael"
    response, latency = make_request(url)
    
    status = "FAIL"
    details = ""
    if response:
        if response.status_code == 200:
            try:
                data = response.json()
                if "name" in data and "age" in data and "count" in data:
                    if isinstance(data["name"], str) and (isinstance(data["age"], int) or data["age"] is None) and isinstance(data["count"], int):
                        status = "PASS"
                    else:
                        details = "Invalid data types"
                else:
                    details = "Missing fields"
            except ValueError:
                details = "Invalid JSON"
        elif response.status_code == 429:
            details = "Rate limited"
        else:
            details = f"Unexpected status code: {response.status_code}"
    else:
        details = "Request failed/timeout"
        
    results.append({"name": "GET /?name=michael", "status": status, "latency_ms": latency, "details": details})
    
    # Test 2: Missing name (should be 422 Unprocessable Entity)
    time.sleep(1) # wait between requests
    url = f"{base_url}"
    response, latency = make_request(url)
    
    status = "FAIL"
    details = ""
    if response:
        if response.status_code == 422:
             status = "PASS"
        elif response.status_code == 429:
            details = "Rate limited"
        else:
            details = f"Unexpected status code: {response.status_code}"
    else:
        details = "Request failed/timeout"
        
    results.append({"name": "GET / (missing name)", "status": status, "latency_ms": latency, "details": details})
    
    # Test 3: Multiple names
    time.sleep(1)
    url = f"{base_url}?name[]=michael&name[]=matthew"
    response, latency = make_request(url)
    
    status = "FAIL"
    details = ""
    if response:
         if response.status_code == 200:
             try:
                 data = response.json()
                 if isinstance(data, list) and len(data) == 2:
                     status = "PASS"
                 else:
                     details = "Expected list of 2 items"
             except ValueError:
                 details = "Invalid JSON"
         elif response.status_code == 429:
             details = "Rate limited"
         else:
             details = f"Unexpected status code: {response.status_code}"
    else:
        details = "Request failed/timeout"
        
    results.append({"name": "GET /?name[]=...", "status": status, "latency_ms": latency, "details": details})
    
    # Test 4: Name with spaces
    time.sleep(1)
    url = f"{base_url}?name=jean+luc"
    response, latency = make_request(url)
    
    status = "FAIL"
    details = ""
    if response:
         if response.status_code == 200:
             status = "PASS"
         elif response.status_code == 429:
             details = "Rate limited"
         else:
             details = f"Unexpected status code: {response.status_code}"
    else:
        details = "Request failed/timeout"
        
    results.append({"name": "GET /?name=with+spaces", "status": status, "latency_ms": latency, "details": details})
    
    # Test 5: Check Content-Type header
    time.sleep(1)
    url = f"{base_url}?name=sarah"
    response, latency = make_request(url)
    
    status = "FAIL"
    details = ""
    if response:
        if response.status_code == 200:
            if "application/json" in response.headers.get("Content-Type", ""):
                 status = "PASS"
            else:
                 details = "Content-Type is not application/json"
        elif response.status_code == 429:
             details = "Rate limited"
        else:
            details = f"Unexpected status code: {response.status_code}"
    else:
        details = "Request failed/timeout"
        
    results.append({"name": "GET /?name=sarah (Content-Type check)", "status": status, "latency_ms": latency, "details": details})
    
    # Test 6: Unknown country code
    time.sleep(1)
    url = f"{base_url}?name=michael&country_id=ZZ"
    response, latency = make_request(url)
    
    status = "FAIL"
    details = ""
    if response:
        # Agify returns 200 even for unknown country codes, but age might be null
        if response.status_code == 200:
            status = "PASS"
        elif response.status_code == 429:
            details = "Rate limited"
        else:
             details = f"Unexpected status code: {response.status_code}"
    else:
        details = "Request failed/timeout"
        
    results.append({"name": "GET /?name=...&country_id=ZZ", "status": status, "latency_ms": latency, "details": details})

    return results
