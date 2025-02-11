import scrapy
import os
import re
from urllib.parse import urlparse

class AstdiffSpider(scrapy.Spider):
    name = "astdiff"
    # If your site is served locally, be sure to list "localhost" (without the port)
    # and any external domains referenced by assets.
    allowed_domains = ["localhost", "cdn.jsdelivr.net", "code.jquery.com"]
    start_urls = ["http://localhost:6789/"]

    def parse(self, response):
        # Save the response (HTML or asset) to a file based on its URL.
        self.save_static(response)

        # Only extract further links if this is an HTML document.
        content_type = response.headers.get('Content-Type', b'').decode('utf8').lower()
        if 'text/html' not in content_type:
            return

        # --- Follow interactive elements ---

        # 1. Follow <a> tags with the .btn-primary class.
        for a in response.css("a.btn-primary"):
            href = a.attrib.get("href")
            if href:
                yield response.follow(href, callback=self.parse)

        # 2. Follow <button> tags with the .btn-primary class.
        for btn in response.css("button.btn-primary"):
            onclick = btn.attrib.get("onclick", "")
            match = re.search(r"location\.href\s*=\s*['\"](.*?)['\"]", onclick)
            if match:
                url = match.group(1)
                yield response.follow(url, callback=self.parse)

        # --- Follow asset links ---

        # Look for common asset tags: <link> for CSS/icons, <script> for JS, and <img> for images.
        asset_tags = [
            ("link", "href"),
            ("script", "src"),
            ("img", "src"),
        ]
        for tag, attr in asset_tags:
            for node in response.css(f"{tag}[{attr}]"):
                asset_url = node.attrib.get(attr)
                if asset_url:
                    # Request assets with the asset callback.
                    yield response.follow(asset_url, callback=self.parse_asset)

    def parse_asset(self, response):
        # Simply save the asset. We do not extract links from assets.
        self.save_static(response)

    def save_static(self, response):
        """
        Save the response body to a file whose path is based on the URL.
        For example:
          http://localhost:6789/                -> output/localhost/index.html
          http://localhost:6789/list            -> output/localhost/list.html
          http://localhost:6789/monaco-page/0/  -> output/localhost/monaco-page/0/index.html
          https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css
                                                -> output/cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css
        """
        file_path = self.get_file_path(response.url)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        self.logger.info("Saving file %s", file_path)
        with open(file_path, "wb") as f:
            f.write(response.body)

    def get_file_path(self, url):
        """
        Compute a local file path for a given URL.
        """
        parsed = urlparse(url)
        path = parsed.path

        # If the URL ends with a slash, assume it's a directory and add index.html.
        if path.endswith("/"):
            path += "index.html"
        # If the URL has no file extension, assume it's an HTML document and append its extension.
        elif not os.path.splitext(path)[1]:
            path += ".html"


        # Remove a leading slash so os.path.join works as intended.
        return os.path.join("output", parsed.netloc, path.lstrip("/"))
