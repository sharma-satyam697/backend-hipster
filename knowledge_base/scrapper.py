import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import time
from typing import List, Dict, Optional
import warnings
warnings.filterwarnings('ignore')

class WebScraper:
    def __init__(self, delay: float = 1.0):
        """
        Initialize the web scraper

        Args:
            delay: Delay between requests in seconds (be respectful to servers)
        """
        self.delay = delay
        self.session = requests.Session()
        # Set a user agent to avoid being blocked
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def get_page_content(self, url: str) -> Optional[str]:
        """
        Fetch the HTML content of a web page

        Args:
            url: The URL to scrape

        Returns:
            HTML content as string or None if failed
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def extract_text_from_html(self, html: str) -> str:
        """
        Extract clean text from HTML content

        Args:
            html: HTML content as string

        Returns:
            Clean text content
        """
        soup = BeautifulSoup(html, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
            script.decompose()

        # Get text content
        text = soup.get_text()

        # Clean up the text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def extract_structured_data(self, html: str) -> Dict:
        """
        Extract structured data from HTML (title, headings, paragraphs, etc.)

        Args:
            html: HTML content as string

        Returns:
            Dictionary with structured data
        """
        soup = BeautifulSoup(html, 'html.parser')

        # Remove unwanted elements
        for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
            script.decompose()

        data = {
            'title': '',
            'headings': [],
            'paragraphs': [],
            'links': [],
            'images': [],
            'meta_description': ''
        }

        # Extract title
        title_tag = soup.find('title')
        if title_tag:
            data['title'] = title_tag.get_text().strip()

        # Extract meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            data['meta_description'] = meta_desc.get('content', '').strip()

        # Extract headings
        for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            data['headings'].append({
                'level': heading.name,
                'text': heading.get_text().strip()
            })

        # Extract paragraphs
        for para in soup.find_all('p'):
            text = para.get_text().strip()
            if text:
                data['paragraphs'].append(text)

        # Extract links
        for link in soup.find_all('a', href=True):
            data['links'].append({
                'text': link.get_text().strip(),
                'url': link['href']
            })

        # Extract images
        for img in soup.find_all('img', src=True):
            data['images'].append({
                'alt': img.get('alt', ''),
                'src': img['src']
            })

        return data

    def scrape_url(self, url: str, return_structured: bool = False) -> Dict:
        """
        Scrape a single URL and return text content

        Args:
            url: URL to scrape
            return_structured: Whether to return structured data or just text

        Returns:
            Dictionary with scraped data
        """

        html = self.get_page_content(url)
        if not html:
            return {'url': url, 'success': False, 'error': 'Failed to fetch content'}

        try:
            if return_structured:
                structured_data = self.extract_structured_data(html)
                return {
                    'url': url,
                    'success': True,
                    'data': structured_data,
                    'raw_text': self.extract_text_from_html(html)
                }
            else:
                text = self.extract_text_from_html(html)
                return {
                    'url': url,
                    'success': True,
                    'text': text,
                    'text_length': len(text)
                }
        except Exception as e:
            return {'url': url, 'success': False, 'error': str(e)}

    def scrape_multiple_urls(self, urls: List[str], return_structured: bool = False) -> List[Dict]:
        """
        Scrape multiple URLs

        Args:
            urls: List of URLs to scrape
            return_structured: Whether to return structured data or just text

        Returns:
            List of dictionaries with scraped data
        """
        results = []

        for i, url in enumerate(urls):
            result = self.scrape_url(url, return_structured)
            results.append(result)

            # Be respectful - add delay between requests
            if i < len(urls) - 1:
                time.sleep(self.delay)

        return results


# URL Extractor Script for Jupyter Notebook
# This script extracts all URLs from a web page

class URLExtractor:
    def __init__(self):
        """Initialize the URL extractor"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def get_page_content(self, url: str) -> Optional[str]:
        """
        Fetch the HTML content of a web page

        Args:
            url: The URL to fetch

        Returns:
            HTML content as string or None if failed
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def extract_urls_from_html(self, html: str, base_url: str) -> List[Dict]:
        """
        Extract all URLs from HTML content

        Args:
            html: HTML content as string
            base_url: Base URL for resolving relative URLs

        Returns:
            List of dictionaries containing URL information
        """
        soup = BeautifulSoup(html, 'html.parser')
        urls = []

        # Find all anchor tags with href attribute
        for link in soup.find_all('a', href=True):
            href = link['href'].strip()

            # Skip empty hrefs and javascript/mailto links
            if not href or href.startswith(('javascript:', 'mailto:', 'tel:', '#')):
                continue

            # Convert relative URLs to absolute URLs
            absolute_url = urljoin(base_url, href)

            # Get link text
            link_text = link.get_text().strip()

            # Get additional attributes
            title = link.get('title', '')
            target = link.get('target', '')

            urls.append({
                'url': absolute_url,
                'original_href': href,
                'link_text': link_text,
                'title': title,
                'target': target,
                'is_internal': self._is_internal_link(absolute_url, base_url),
                'is_relative': not bool(urlparse(href).netloc)
            })

        return urls

    def _is_internal_link(self, url: str, base_url: str) -> bool:
        """
        Check if a URL is internal (same domain) or external

        Args:
            url: URL to check
            base_url: Base URL for comparison

        Returns:
            True if internal, False if external
        """
        try:
            url_domain = urlparse(url).netloc.lower()
            base_domain = urlparse(base_url).netloc.lower()
            return url_domain == base_domain
        except:
            return False

    def get_all_urls(self, url: str, filter_options: Dict = None) -> Dict:
        """
        Extract all URLs from a web page with filtering options

        Args:
            url: URL to extract links from
            filter_options: Dictionary with filtering options

        Returns:
            Dictionary containing extracted URLs and metadata
        """
        if filter_options is None:
            filter_options = {}

        print(f"Extracting URLs from: {url}")

        html = self.get_page_content(url)
        if not html:
            return {'success': False, 'error': 'Failed to fetch content'}

        try:
            urls = self.extract_urls_from_html(html, url)

            # Apply filters
            filtered_urls = self._apply_filters(urls, filter_options)

            # Remove duplicates while preserving order
            unique_urls = []
            seen = set()
            for url_info in filtered_urls:
                if url_info['url'] not in seen:
                    unique_urls.append(url_info)
                    seen.add(url_info['url'])

            # Separate internal and external links
            internal_links = [u for u in unique_urls if u['is_internal']]
            external_links = [u for u in unique_urls if not u['is_internal']]

            return {
                'success': True,
                'source_url': url,
                'total_links': len(unique_urls),
                'internal_links': len(internal_links),
                'external_links': len(external_links),
                'all_urls': unique_urls,
                'internal_urls': internal_links,
                'external_urls': external_links
            }

        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _apply_filters(self, urls: List[Dict], filter_options: Dict) -> List[Dict]:
        """
        Apply filtering options to the URL list

        Args:
            urls: List of URL dictionaries
            filter_options: Filtering options

        Returns:
            Filtered list of URLs
        """
        filtered = urls

        # Filter by internal/external
        if filter_options.get('internal_only'):
            filtered = [u for u in filtered if u['is_internal']]
        elif filter_options.get('external_only'):
            filtered = [u for u in filtered if not u['is_internal']]

        # Filter by URL pattern
        if filter_options.get('include_pattern'):
            pattern = filter_options['include_pattern']
            filtered = [u for u in filtered if re.search(pattern, u['url'], re.IGNORECASE)]

        # Exclude by URL pattern
        if filter_options.get('exclude_pattern'):
            pattern = filter_options['exclude_pattern']
            filtered = [u for u in filtered if not re.search(pattern, u['url'], re.IGNORECASE)]

        # Filter by file extensions
        if filter_options.get('exclude_files'):
            file_extensions = filter_options['exclude_files']
            if isinstance(file_extensions, str):
                file_extensions = [file_extensions]

            for ext in file_extensions:
                filtered = [u for u in filtered if not u['url'].lower().endswith(f'.{ext.lower()}')]

        # Filter out common non-content URLs
        if filter_options.get('exclude_common_files', True):
            common_extensions = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',
                                 'zip', 'rar', 'tar', 'gz', 'jpg', 'jpeg', 'png', 'gif',
                                 'svg', 'mp4', 'mp3', 'avi', 'mov', 'css', 'js']

            for ext in common_extensions:
                filtered = [u for u in filtered if not u['url'].lower().endswith(f'.{ext}')]

        return filtered


# Convenience functions for easy use
def extract_urls_from_page(url: str, **filter_options) -> Dict:
    """
    Extract all URLs from a web page

    Args:
        url: URL to extract links from
        **filter_options: Filtering options (internal_only, external_only, etc.)

    Returns:
        Dictionary containing extracted URLs and metadata
    """
    extractor = URLExtractor()
    return extractor.get_all_urls(url, filter_options)


def get_internal_urls(url: str, exclude_files: bool = True) -> List[str]:
    """
    Get only internal URLs from a page (same domain)

    Args:
        url: URL to extract links from
        exclude_files: Whether to exclude file downloads

    Returns:
        List of internal URLs
    """
    result = extract_urls_from_page(url, internal_only=True, exclude_common_files=exclude_files)
    if result['success']:
        return [u['url'] for u in result['internal_urls']]
    return []


def get_external_urls(url: str, exclude_files: bool = True) -> List[str]:
    """
    Get only external URLs from a page (different domain)

    Args:
        url: URL to extract links from
        exclude_files: Whether to exclude file downloads

    Returns:
        List of external URLs
    """
    result = extract_urls_from_page(url, external_only=True, exclude_common_files=exclude_files)
    if result['success']:
        return [u['url'] for u in result['external_urls']]
    return []


def scrape_all(urls: List[str], return_structured: bool = False, delay: float = 1.0) -> List[Dict]:
    """
    Scrape multiple URLs and return the results

    Args:
        urls: List of URLs to scrape
        return_structured: Whether to return structured data or just text
        delay: Delay between requests in seconds

    Returns:
        List of dictionaries with scraped data
    """
    scraper = WebScraper(delay=delay)
    return scraper.scrape_multiple_urls(urls, return_structured)




