from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

from selenium.webdriver.support.wait import WebDriverWait


# Function to save played video link and duration to a file
def log_played_video(link, duration, file="played.txt"):
    with open(file, "a") as file:
        file.write(f"{link} - {duration} seconds\n")


def open_and_play_videos(links_file, played_file):
    """
    Opens links from a text file one by one, plays videos (assuming they are within elements with the specified class),
    and waits for each video to finish before moving to the next link.

    Args:
        links_file (str): Path to the text file containing video links (one per line).
        class_name (str, optional): The class name of the elements containing the videos (default: "style-scope ytd-grid-video-renderer").
    """

    with open(links_file, 'r') as f:
        links = f.readlines()

    for link in links:

        options = webdriver.EdgeOptions()
        options.add_argument('--ignore-certificate-errors')
        driver = webdriver.Edge(options=options)

        driver.get(link.strip())  # Remove leading/trailing whitespace

        # Bring the window into focus
        driver.switch_to.window(driver.current_window_handle)

        # Track the start time
        start_time = time.time()

        print(f"Opening video: {link.strip()}")
        try:
            # Wait for video player to become clickable
            WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'ytp-play-button'))
            ).click()

            # Check every minute and click play if button title is "Play (k)"
            canExit = True
            while canExit:
                play_button = driver.find_element(By.CLASS_NAME, 'ytp-play-button')
                print(play_button.get_attribute('title'))
                if play_button.get_attribute('title') == 'Play (k)':
                    print("Is is stopped...???  Yes, it is stopped...!!! Playing now...!!!")
                    play_button.click()

                # Check if the end screen content is displayed
                try:
                    WebDriverWait(driver, 2).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, 'ytp-autonav-endscreen-upnext-header'))
                    )
                    print("End screen detected")
                    canExit = False
                except:
                    print("Just passing by")
                    pass

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Track the end time
            end_time = time.time()
            duration_seconds = end_time - start_time
            duration_minutes = duration_seconds / 60
            log_played_video(link.strip(), duration_minutes, played_file)

            driver.quit()
            time.sleep(10)  # Optional delay between videos (adjust as needed)
            driver.quit()
            time.sleep(10)  # Optional delay between videos (adjust as needed)


# Example usage:
links_talha = "video_links_talha.txt"
links_mubashir = "video_links_mubashir.txt"

if __name__ == "__main__":
    open_and_play_videos(links_talha, "played_talha.txt")
    open_and_play_videos(links_mubashir, "played_mubashir.txt")
