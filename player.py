import json
import os
import threading

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

cookiePopup = True  # Set to True if the cookie popup appears
CHECK_INTERVAL = 2  # Interval to check play status in seconds
TIMEOUT = 120  # Timeout to restart video if no activity in seconds


class WatchdogTimer:
    def __init__(self, timeout, callback):
        self.timeout = timeout
        self.callback = callback
        self.timer = None

    def reset(self):
        self.cancel()
        self.timer = threading.Timer(self.timeout, self.callback)
        self.timer.start()

    def cancel(self):
        if self.timer:
            self.timer.cancel()
            self.timer = None


def log_played_video(link, duration, file="played.json"):
    # Load the existing data from the JSON file
    if os.path.exists(file):
        with open(file, 'r') as f:
            played_data = json.load(f)
    else:
        played_data = {}

    # Update the play count and duration
    if link in played_data:
        played_data[link]['count'] += 1
        played_data[link]['total_duration'] += duration
    else:
        played_data[link] = {'count': 1, 'total_duration': duration}

    # Save the updated data back to the JSON file
    with open(file, 'w') as f:
        json.dump(played_data, f, indent=4)


def play_video(driver, link, watchdog):
    """
    Plays the video and waits for it to finish.

    Args:
        driver: The webdriver instance.
        link: The video link to be played.
    """
    try:
        driver.get(link.strip())  # Remove leading/trailing whitespace

        # Bring the window into focus
        driver.switch_to.window(driver.current_window_handle)

        # Handle the cookie popup if necessary
        if cookiePopup:
            try:
                time.sleep(2)
                # Click on 'Accept all' button
                buttons = driver.find_elements(By.CLASS_NAME, 'yt-spec-button-shape-next')
                for button in buttons:
                    if button.get_attribute(
                            'aria-label') == 'Accept the use of cookies and other data for the purposes described':
                        button.click()
                        break
                print("Clicked on 'Accept all' button.")
            except Exception as e:
                print(f"An error occurred while handling cookie popup: {e}")

        # Start the watchdog timer before waiting for the element
        watchdog.reset()

        # Wait for video player to become clickable
        WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'ytp-play-button'))
        ).click()

        # Check every minute and click play if button title is "Play (k)"
        canExit = True
        while canExit:
            play_button = driver.find_element(By.CLASS_NAME, 'ytp-play-button')
            print(play_button.get_attribute('title'))
            if play_button.get_attribute('title') == 'Pause (k)':
                print("Video is playing... Waiting for it to finish...")
                watchdog.reset()  # Reset the watchdog timer
            if play_button.get_attribute('title') == 'Play (k)':
                print("Video is stopped... Playing now...!!!")
                play_button.click()

            # Check if the end screen content is displayed
            try:
                WebDriverWait(driver, 2).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, 'ytp-autonav-endscreen-upnext-header'))
                )
                print("End screen detected")
                canExit = False
            except:
                print("Continuing to play...")
                pass

    except Exception as e:
        print(f"An error occurred during video play: {e}")
        raise  # Re-raise the exception to handle it in the outer try-except


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
        start_time = time.time()

        while True:
            options = webdriver.EdgeOptions()
            options.add_argument('--ignore-certificate-errors')
            driver = webdriver.Edge(options=options)

            def on_timeout():
                print("Timeout: Video stuck or not detected. Restarting the video...")
                driver.quit()
                # stop timer and raise exception
                watchdog.cancel()
                raise Exception("Timeout: Video stuck or not detected.")

            watchdog = WatchdogTimer(TIMEOUT, on_timeout)

            try:
                play_video(driver, link, watchdog)
                break  # Exit loop if video plays successfully
            except Exception as e:
                print(f"An error occurred: {e}. Restarting the video...")
                driver.quit()
                time.sleep(10)  # Optional delay before retrying

        # Track the end time
        end_time = time.time()
        duration_seconds = end_time - start_time
        duration_minutes = duration_seconds / 60
        log_played_video(link.strip(), duration_minutes, played_file)

        driver.quit()
        time.sleep(10)  # Optional delay between videos (adjust as needed)


# Example usage:
links_talha = "video_links_talha.txt"
links_mubashir = "video_links_mubashir.txt"
links_snooker = "video_links_snooker.txt"

if __name__ == "__main__":
    for _ in range(10):
        open_and_play_videos(links_talha, "played_talha.json")
        open_and_play_videos(links_snooker, "played_snooker.json")
        open_and_play_videos(links_mubashir, "played_mubashir.json")
