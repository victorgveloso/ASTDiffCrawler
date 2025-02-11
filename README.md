# ASTCrawler

A minimalistic Python crawler designed for ASTDiff GUI exploration and static asset preservation.

## Installation

Install from source:

```bash
pip install .
```

For development mode (hot-reload):

```bash
pip install -e .
```

## Usage

### As installed package

```bash
python -m astcrawler
```

### Without installation (from project root)

Activate virtual environment:

```bash
source venv/bin/activate
```

Run directly using Scrapy:

```bash
scrapy crawl astdiff
```


## Configuration

The crawler is pre-configured with:
- Local development server support (`localhost:6789`)
- Common CDN domains whitelisted
- HTTP caching enabled (stored in `httpcache/`)
- Output files saved to `output/` directory

To modify settings, edit `src/astcrawler/settings.py`.

## Folder Structure

```
src/astcrawler/
├── spiders/
│ └── astdiff_spider.py # Main crawler logic (lines 6-89)
├── main.py # CLI entrypoint (lines 7-15)
├── settings.py # Cache/config settings (lines 1-12)
└── ... # Other Scrapy boilerplate
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit changes with descriptive messages
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

Please ensure tests are updated/added for new features. Run existing tests (if any) with:

```bash
python -m pytest tests/
```