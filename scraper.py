from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Function to scroll down to load all videos
def scroll_to_load_all_videos(driver):
    # Scroll to the bottom of the page multiple times to load all videos
    for _ in range(10):  # Adjust the range as needed
        driver.find_element(by='tag name', value='body').send_keys(Keys.END)
        time.sleep(2)  # Adjust sleep time as needed


# Function to scrape video links from YouTube channel page
def scrape_youtube_channel_videos(channel_url):
    # Configure Selenium webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--incognito')
    # options.add_argument('--headless')  # Optional: run headless
    driver = webdriver.Chrome(options=options)

    # Send a GET request to the channel URL
    driver.get(channel_url)

    # Scroll down to load all videos
    scroll_to_load_all_videos(driver)

    links = []

    # Find all video links using Class
    video_links = driver.find_elements(
        by='id', value='video-title-link')
    for link in video_links:
        links.append(link.get_attribute('href'))

    # Close the webdriver
    driver.quit()

    return links


# Main function
def main():
    # YouTube channel URL
    channel_url = "https://www.youtube.com/@talhafakhar/videos"

    # Scrape video links from the channel page
    video_urls = scrape_youtube_channel_videos(channel_url)

    # Write video URLs to a text file
    if video_urls:
        with open("video_links_talha.txt", "w") as file:
            for url in video_urls:
                file.write(url + "\n")
        print("Video links saved to video_links_talha.txt")
    else:
        print("No video links found.")

    # YouTube channel URL
    channel_url = "https://www.youtube.com/@MubashirFaisal/videos"

    # Scrape video links from the channel page
    video_urls = scrape_youtube_channel_videos(channel_url)

    # Write video URLs to a text file
    if video_urls:
        with open("video_links_mubashir.txt", "w") as file:
            for url in video_urls:
                file.write(url + "\n")
        print("Video links saved to video_links_mubashir.txt")
    else:
        print("No video links found.")

    # YouTube channel URL
    channel_url = "https://www.youtube.com/@Snooker00/videos"

    # Scrape video links from the channel page
    video_urls = scrape_youtube_channel_videos(channel_url)

    # Write video URLs to a text file
    if video_urls:
        with open("video_links_snooker.txt", "w") as file:
            for url in video_urls:
                file.write(url + "\n")
        print("Video links saved to video_links_snooker.txt")
    else:
        print("No video links found.")


# Entry point of the script
if __name__ == "__main__":
    main()
