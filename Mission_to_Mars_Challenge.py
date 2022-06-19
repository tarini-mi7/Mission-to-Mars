
from bs4 import BeautifulSoup as soup


def scrape_hemisphere_data(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.full-content', wait_time=5)
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    hemisphere_soup = soup(html, 'html.parser')
    full_content_elem = hemisphere_soup.select_one('div.full-content')
    
    def get_full_image_url(thumbnail) -> str:
        thumbnail.click()
        browser.is_element_present_by_css('div.wrapper', wait_time=1)
        page_html = browser.html
        page_soup = soup(page_html, 'html.parser')
        downloads_elem = page_soup.find('div', class_='downloads')
        sample_elem = downloads_elem.find_all('li')[0]
        full_image_url = sample_elem.find('a').get('href')
        browser.back()
        return full_image_url

    for i in range(4):
        item_dict = dict()
        item_elem = browser.find_by_css('.item')[i]

        # extract title
        hemisphere_title = item_elem.find_by_tag('h3')[0].html
        print(hemisphere_title)
        item_dict["title"] = hemisphere_title
        
        # extract absolute image 
        thumbnail = item_elem.find_by_tag('a')[1]
        rel_image_url = get_full_image_url(thumbnail)
        full_image_url = f'{url}{rel_image_url}'
        print(full_image_url)
        item_dict["img_url"] = full_image_url
        hemisphere_image_urls.append(item_dict)

    return hemisphere_image_urls