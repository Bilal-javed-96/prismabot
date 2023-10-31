from langchain.document_loaders import SitemapLoader

import bs4
from bs4 import BeautifulSoup
# fixes a bug with asyncio and jupyter
import nest_asyncio

nest_asyncio.apply()

def docs_extractor(soup: BeautifulSoup) -> str:
    # Find and extract <h1> content
    h1_tag = soup.find('h1', class_='article-title')
    h1_content = h1_tag.text.strip() if h1_tag else "No <h1> found"
    # Find main content section
    section_tag = soup.find('section', class_='gh-content')
    final_content = ""
    for el in section_tag:
        if isinstance(el, bs4.element.Tag):
            tag = el.name
            if tag == "h1":
                final_content += f"# {el.text}\n"
            elif tag == "h2":
                final_content += f"## {el.text}\n"
            elif tag == "h3":
                final_content += f"### {el.text}\n"
            elif tag == "h4":
                final_content += f"#### {el.text}\n"
            elif tag == "h5":
                final_content += f"##### {el.text}\n"
            elif tag == "h6":
                final_content += f"###### {el.text}\n"
            elif tag == "p":
                final_content += f"{el.text}\n"
            elif tag == "ul":
                final_content += "- " + \
                    "\n- ".join(li.text for li in el.find_all('li')) + "\n"
            elif tag == 'b':
                final_content += f"**{el.text}**"
            elif tag == 'i':
                final_content += f"*{el.text}*"
            elif tag == 'pre' or tag == 'code':
                final_content += f"{el.text}\n"
            # Handle tables
            elif tag == 'table':
                table_content = ""
                for row in el.find_all('tr'):
                    row_content = ""
                    for cell in row.find_all(['td', 'th']):
                        row_content += cell.text + " | "
                    table_content += row_content + "\n"
                final_content += f"{table_content}\n"

            # Handle links
            elif tag == 'a':
                link_text = el.text
                link_url = el['href']
                final_content += f"[{link_text}]({link_url})"

    final_content = f"# {h1_content}\n\n{final_content}"
    return final_content.strip()


docs = SitemapLoader(
    "https://blog.chainflip.io/sitemap-posts.xml",
    filter_urls=[r'https://blog.chainflip.io/(?!.*(?:kr|ru|cn)).*'],
    parsing_function=docs_extractor,
).load()