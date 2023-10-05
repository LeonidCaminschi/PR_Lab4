import socket
from bs4 import BeautifulSoup


def parse_products_html(html_content):
    products_list = []

    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all <ul> tags containing product information
    ul_tags = soup.find_all('ul')

    for ul_tag in ul_tags:
        product_dict = {}
        li_tags = ul_tag.find_all('li')
        for li in li_tags:
            key, value = li.get_text().split(': ', 1)
            if key and value:
                product_dict[key] = value
        products_list.append(product_dict)

    return products_list


def parse_tcp_packet(url, port, endpoint):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((url, port))

        s.settimeout(2)

        request = f"GET {endpoint} HTTP/1.1\r\nHost: {url}\r\n\r\n"
        s.send(request.encode())

        if endpoint.__contains__("product"):
            print(parse_products_html(s.recv(2048).decode("utf-8")))
        else:
            print(s.recv(2048).decode("utf-8"))

        s.close()
    except Exception as e:
        print(f"Error occurred please analyze the exception :) {str(e)}")


url = "127.0.0.1"
port = 8081

parse_tcp_packet(url, port, "/products")
parse_tcp_packet(url, port, "/product/1")
parse_tcp_packet(url, port, "/product/2")
parse_tcp_packet(url, port, "/")
parse_tcp_packet(url, port, "/contacts")
parse_tcp_packet(url, port, "/about")