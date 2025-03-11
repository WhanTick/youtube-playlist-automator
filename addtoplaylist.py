# agak bermasalah (harus pencet n buat lanjut)

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import undetected_chromedriver as uc
import keyboard
import threading


skip_to_next = False


def setup_driver():

    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    )
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = uc.Chrome(options=options, version_main=133)
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
        },
    )
    return driver


def login_to_youtube(driver, email, password):

    try:
        driver.get("https://accounts.google.com/signin")
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        )
        email_input.send_keys(email)
        driver.find_element(By.ID, "identifierNext").click()
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_input.send_keys(password)
        driver.find_element(By.ID, "passwordNext").click()
        time.sleep(5)
        print("Logged in successfully")
    except Exception as e:
        print(f"Login failed: {e}")
        driver.quit()
        raise


def add_video_to_playlist(
    driver, video_url, playlist_url, playlist_name="Videogame Music"
):

    try:
        driver.get(video_url)
        time.sleep(2)

        save_button = WebDriverWait(driver, 99999).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@aria-label='Save to playlist']")
            )
        )
        save_button.click()

        playlist_dialog = WebDriverWait(driver, 99999).until(
            EC.presence_of_element_located(
                (By.XPATH, "//tp-yt-paper-dialog[@role='dialog']")
            )
        )

        playlist_items = driver.find_elements(
            By.XPATH, "//ytd-playlist-add-to-option-renderer"
        )
        playlist_found = False

        for item in playlist_items:
            playlist_name_attr = item.find_element(
                By.XPATH, ".//yt-formatted-string[@id='label']"
            ).get_attribute("title")
            if playlist_name_attr == playlist_name:
                item.find_element(By.XPATH, ".//div[@id='checkbox']").click()
                playlist_found = True
                break

        if not playlist_found:
            print(f"Playlist '{playlist_name}' not found for video: {video_url}")
            return False

        done_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Save']"))
        )
        done_button.click()

        print(f"Successfully added video {video_url} to playlist")
        return True

    except TimeoutException:
        print(f"Timeout error adding video {video_url}")
        return False
    except NoSuchElementException:
        print(f"Element not found for video {video_url}")
        return False
    except Exception as e:
        print(f"Error adding video {video_url}: {e}")
        return False


def listen_for_hotkey():

    global skip_to_next
    while True:
        if keyboard.is_pressed("ctrl+n"):
            skip_to_next = True
            print("Hotkey pressed: Skipping to next video...")
            time.sleep(0.5)
        elif keyboard.is_pressed("n"):
            skip_to_next = True
            print("Hotkey pressed: Skipping to next video...")
            time.sleep(0.5)


def main():
    global skip_to_next
    driver = setup_driver()

    hotkey_thread = threading.Thread(target=listen_for_hotkey, daemon=True)
    hotkey_thread.start()

    driver.get("https://www.youtube.com")
    print("Please log into YouTube in the browser, then press Enter to continue...")
    print("Hotkeys: Press 'Ctrl+N' or 'N' to skip to the next video.")
    input()

    try:
        with open("youtubeIdList.txt", "r") as file:
            video_ids = [line.strip() for line in file if line.strip()]

        if not video_ids:
            print("No video IDs found in youtubeIdList.txt")
            driver.quit()
            return

        playlist_url = "your playlist url"
        playlist_name = "your playlist name"
        successful = 0
        failed = 0

        for video_id in video_ids:
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            print(f"\nProcessing video: {video_url}")

            if skip_to_next:
                print(f"Skipping video {video_url} due to hotkey press")
                skip_to_next = False  # Reset the flag
                failed += 1
                continue

            if add_video_to_playlist(driver, video_url, playlist_url, playlist_name):
                successful += 1
            else:
                failed += 1

            if skip_to_next:
                print(
                    f"Skipping remaining actions for video {video_url} due to hotkey press"
                )
                skip_to_next = False
                failed += 1
                continue

            time.sleep(2)

        print("\nSummary:")
        print(f"Successfully added: {successful} videos")
        print(f"Failed: {failed} videos (including skipped)")

    except FileNotFoundError:
        print("Error: youtubeIdList.txt not found")
    except Exception as e:
        print(f"Error reading video IDs: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
