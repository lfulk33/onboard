from bs4 import BeautifulSoup

def strip_html(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    return soup.get_text(separator=" ", strip=True)

if __name__ == "__main__":
    html_text="<html><head>this is the head</head><main><h1>Header</h2><p>this is our paragraph</p></main></html>"
    print(strip_html(html_text))