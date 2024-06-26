import os
import requests
import urllib3
from urllib.parse import urlparse, urljoin
import re
from shortuuid import uuid

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


FILES_DIR = os.getenv("FILES_DIR", "/tmp/files")


def _extract_redirect_url(content) -> str | None:
    # Regular expression to find the URL set in window.location.href
    url_pattern = r"window\.location\.href\s*=\s*'([^']+)'"
    match = re.search(url_pattern, content)
    if match:
        return match.group(1)
    return None


def get_encoded_url_file(url: str) -> str | None:
    try:
        api_return = requests.get(url, verify=False)
        if api_return.status_code != 200:
            return None

        api_content = api_return.content.decode()
        redirect_url = _extract_redirect_url(api_content)

        if redirect_url:
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            new_url = urljoin(base_url, redirect_url)
            return new_url
        return None
    except Exception as e:
        print(e)
        return None


def get_file_content(url: str) -> str | None:
    try:
        api_return = requests.get(url, verify=False)
        if api_return.status_code != 200:
            return None

        content_type = api_return.headers.get("Content-Type")

        if content_type is None:
            print("Content-Type not found")
            return None
        elif "application/pdf" in content_type:
            file_extension = ".pdf"
        elif "image/" in content_type:
            file_extension = ".jpg"  # TODO: Check for other image types
        else:
            print(f"Unsupported content type: {content_type}")
            return None

        file_name = f"{uuid()}{file_extension}"
        file_path = os.path.join(FILES_DIR, file_name)
        os.makedirs(FILES_DIR, exist_ok=True)
        print(file_path)

        with open(file_path, "wb") as file:
            file.write(api_return.content)

        return file_path
    except Exception as e:
        print(e)
        return None


def remove_file(path: str) -> None:
    os.unlink(path)


def get_encoded_file(
    url: str,
):
    encoded_url = get_encoded_url_file(url)
    if encoded_url is None:
        return None

    file_path = get_file_content(encoded_url)
    if file_path is None:
        return None

    return file_path
