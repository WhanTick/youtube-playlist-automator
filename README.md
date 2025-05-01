# YouTube Playlist Automator

A Python application that automates adding YouTube videos to a playlist using Selenium and Google's YouTube API. This tool simplifies managing playlists by automatically fetching video IDs based on music titles and adding them to your desired YouTube playlist.

## Features

- Automatically search and retrieve YouTube video IDs using music titles.
- Add videos automatically to your YouTube playlists.
- Supports interruption via hotkeys (`Ctrl+N` or `N`) to skip videos.
- Easily customizable with your own music preferences.

## Requirements

- Python 3.8 or newer
- `aiohttp`, `keyboard`, `python-dotenv`, `selenium`, and `undetected_chromedriver` Python packages
- Chrome browser
- YouTube Data API key (for video searching)

## Installation

### Step 1: Clone Repository

Clone the repository or download the files directly:

```bash
git clone https://github.com/WhanTick/youtube-playlist-automator.git
cd youtube-playlist-automator
```

### Step 2: Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Step 3: Configure API Key

- Obtain your YouTube Data API key from [Google Developers Console](https://console.cloud.google.com/).
- Create a `.env` file in the root directory of the project and add your API key:

```
API_KEY=your_youtube_api_key_here
```

## Preparing Music List

1. Create a file named `musiclist.txt` and list your music titles. Here's an example:

```
Your Song Title 1 [00:00]
Your Song Title 2 [00:00]
```

2. Clean and format your list by running:

```bash
python cleanlist.py
```

3. Generate YouTube video IDs from your cleaned list:

```bash
python getyoutubelink.py
```

This will generate `youtubeIdList.txt` containing video IDs.

> **Note:** The provided `musiclist.txt` and `youtubeIdList.txt` files are just examples. Replace them with your own preferred music titles.

## Usage

Run the playlist automation script:

```bash
python addtoplaylist.py
```

- You must manually log into your YouTube account when prompted.
- After logging in, press Enter in the console to start adding videos to your playlist.
- Use hotkeys (`Ctrl+N` or `N`) to skip videos during automation.

## Customization

Edit the `playlist_url` and `playlist_name` variables in `addtoplaylist.py` to match your own YouTube playlist details:

```python
playlist_url = "your_playlist_url"
playlist_name = "Your Playlist Name"
```

## Troubleshooting

- Ensure you have a stable internet connection.
- Confirm your YouTube Data API key is correctly set in `.env`.
- Check Chrome browser compatibility with `undetected_chromedriver`.

## License

This project is licensed under the MIT License. See `LICENSE` for details.

---

Enjoy managing your playlists effortlessly! 🎶📺🚀

