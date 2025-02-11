import scrapy
import os
import re
from urllib.parse import urlparse

class AstdiffSpider(scrapy.Spider):
    name = "astdiff"
    allowed_domains = ["127.0.0.1:6789"]
    start_urls = ["http://127.0.0.1:6789/"]

    def parse(self, response):
        # Save the response locally to build a static site
        self.save_static(response)

        # Process <a> tags with the .btn-primary class
        for a in response.css("a.btn-primary"):
            href = a.attrib.get("href")
            if href:
                yield response.follow(href, callback=self.parse)

        # Process <button> tags with the .btn-primary class
        for btn in response.css("button.btn-primary"):
            onclick = btn.attrib.get("onclick", "")
            # Look for a common pattern, e.g., location.href='some_url';
            match = re.search(r"location\.href\s*=\s*['\"](.*?)['\"]", onclick)
            if match:
                url = match.group(1)
                yield response.follow(url, callback=self.parse)

    def save_static(self, response):
        """Save the response body to a file path based on its URL."""
        file_path = self.get_file_path(response.url)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        self.logger.info("Saving file %s", file_path)
        with open(file_path, "wb") as f:
            f.write(response.body)


    def get_file_path(self, url):
        """
        Create a file path for the URL.
        For example, https://astdiff.com/ -> output/astdiff.com/index.html
        """
        parsed = urlparse(url)
        path = parsed.path

        # If the URL ends with a slash or has no extension, save as index.html
        if path.endswith("/"):
            path += "index.html"
        elif not os.path.splitext(path)[1]:
            path += "/index.html"

        # Remove any leading slashes for proper os.path.join behavior
        return os.path.join("output", parsed.netloc, path.lstrip("/"))
