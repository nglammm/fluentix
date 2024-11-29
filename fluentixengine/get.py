import urllib3
import os
import sys
from colorama import Fore, Style, init # colored text baby
init(autoreset=True)

def do():
    # URL of the publicly shared Google Doc
    url = 'https://docs.google.com/document/d/1Di02NRP8SShJrGzHVssNoLsSphw114x9Q8LZK1hprv4/export?format=txt'

    # Create an HTTP client
    http = urllib3.PoolManager()

    # Make a request to get the document
    response = http.request('GET', url)

    # Check the response
    if response.status == 200:
        document_content = response.data.decode('utf-8-sig')
        # Save the JSON structure to file.json
        with open(os.path.dirname(os.path.abspath(__file__)) + "/file.json", 'w', encoding='utf-8') as file:
            file.write(document_content)
        

        sys.stdout.write(Fore.GREEN + "\n[SUCCESS]" + Fore.Yellow + "Fetch data success!")
        return True
    else:
        print(Fore.RED + f'[ERROR] Failed to retrieve document: {response.status} - {response.data.decode("utf-8")}')
        return False
