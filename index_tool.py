import requests
from bs4 import BeautifulSoup
import urllib.parse
import os

def get_relative_path(full_url, base_url):
    # Get the relative path of full_url with respect to base_url
    base_path = urllib.parse.urlparse(base_url).path
    full_path = urllib.parse.urlparse(full_url).path
    if full_path.startswith(base_path):
        relative = full_path[len(base_path):]
    else:
        relative = full_path
    return relative.lstrip('/')

def list_files(url, path_list, base_url, visited_urls):
    # Avoid processing the same URL more than once
    if url in visited_urls:
        return
    visited_urls.add(url)
    print(f"Fetching: {url}")
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error accessing {url}: {response.status_code}")
            return
        soup = BeautifulSoup(response.text, 'html.parser')
        # Iterate through all <a> tags
        for link in soup.find_all('a'):
            href = link.get('href')
            if not href:
                continue
            # Skip parent directory links
            if href in ['../', './']:
                continue
            full_link = urllib.parse.urljoin(url, href)
            # Ensure the link is within the base_url
            if not full_link.startswith(base_url):
                continue
            # Get relative path and decode URL-encoded characters
            relative_path = get_relative_path(full_link, base_url)
            decoded_path = urllib.parse.unquote(relative_path)
            if href.endswith('/'):
                # Record the directory relative path (if not already in the list)
                if decoded_path not in path_list:
                    path_list.append(decoded_path)
                # Recursively list the directory
                list_files(full_link, path_list, base_url, visited_urls)
            else:
                # Record file relative path
                path_list.append(decoded_path)
    except Exception as e:
        print(f"Error processing {url}: {e}")

def download_files(url, local_base, base_url, visited_urls):
    # Avoid processing the same URL more than once
    if url in visited_urls:
        return
    visited_urls.add(url)
    print(f"Fetching: {url}")
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error accessing {url}: {response.status_code}")
            return
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a'):
            href = link.get('href')
            if not href:
                continue
            if href in ['../', './']:
                continue
            full_link = urllib.parse.urljoin(url, href)
            if not full_link.startswith(base_url):
                continue
            if href.endswith('/'):
                # Create local directory and recursively download contents
                relative_path = get_relative_path(full_link, base_url)
                local_directory = os.path.join(local_base, relative_path)
                os.makedirs(local_directory, exist_ok=True)
                download_files(full_link, local_base, base_url, visited_urls)
            else:
                # Download the file and save to proper local path
                relative_path = get_relative_path(full_link, base_url)
                local_file_path = os.path.join(local_base, relative_path)
                os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
                download_file(full_link, local_file_path)
    except Exception as e:
        print(f"Error processing {url}: {e}")

def download_file(file_url, local_file_path):
    print(f"Downloading file: {file_url}")
    try:
        response = requests.get(file_url, stream=True)
        if response.status_code == 200:
            with open(local_file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        else:
            print(f"Error downloading {file_url}: {response.status_code}")
    except Exception as e:
        print(f"Error downloading {file_url}: {e}")

def main():
    print("Select operation mode:")
    print("1. List files and directories")
    print("2. Download files (preserving directory structure)")
    mode = input("Enter option number (1/2): ")

    base_url = input("Enter index URL (e.g., http://example.com/test/): ")
    if not base_url.endswith('/'):
        base_url += '/'

    if mode == "1":
        path_list = []
        visited_urls = set()
        list_files(base_url, path_list, base_url, visited_urls)
        with open("file_list.txt", "w", encoding="utf-8") as f:
            for path in path_list:
                f.write(path + "\n")
        print("File list saved in 'file_list.txt'.")
    elif mode == "2":
        local_base = input("Enter local download directory (e.g., ./downloaded_files): ")
        if not os.path.exists(local_base):
            os.makedirs(local_base)
        visited_urls = set()
        download_files(base_url, local_base, base_url, visited_urls)
        print("Download completed.")
    else:
        print("Invalid option. Exiting.")

if __name__ == '__main__':
    main()
