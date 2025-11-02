#!/usr/bin/env python3
import json
import requests

URL = "https://hayahora.futbol/estado/data.json"

def get_ips():
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        filtered_ips = set()
        
        for ip_group in data['data']:
            ip = ip_group['ip']
            state_changes = ip_group.get('stateChanges', [])
            
            if state_changes and state_changes[-1]['state']:
                filtered_ips.add(ip)
        
        ips = sorted(filtered_ips)
        
        if not ips:
            print("Warning: No IPs found")
        
        # Write to file
        with open('blocked-ips.txt', 'w') as f:
            for ip in ips:
                f.write(f"{ip}\n")
        
        print(f"Successfully updated blocked-ips.txt with {len(ips)} IPs")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = get_ips()
    exit(0 if success else 1)