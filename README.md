# MediaHub Desktop

MediaHub Desktop is a Flask-based media utility application that allows users to fetch and download video or audio content from supported links using yt-dlp.  
It supports single videos, playlists, quality selection, MP3 conversion, and download management through a clean desktop-friendly web interface.

---

# Disclaimer

This project is for educational purposes only.

Users are responsible for complying with:
- Platform Terms of Service
- Copyright laws
- Local regulations regarding media downloading and usage

The developer of this project does not encourage piracy or unauthorized distribution of copyrighted content.

---
# Deployed as UI demo
https://mediafetcher-desktop.onrender.com/

Cloud deployments may face YouTube bot-detection restrictions.

To use needed to run as local.

---
# Features

## Single Video Download
- Download individual videos
- Choose available video quality
- View estimated file size before downloading

## Audio Download
- Convert and download audio as MP3
- Powered by FFmpeg integration

## Playlist Support
- Fetch playlist videos
- Select specific videos to download
- Apply common quality/audio settings to selected items

## Download Controls
- Cancel ongoing downloads
- Background threaded downloading

## User Interface
- Thumbnail previews
- Responsive grid layout
- Simple desktop-friendly UI

---

# Tech Stack

## Backend
- Python
- Flask
- yt-dlp
- FFmpeg

## Frontend
- HTML5
- CSS3
- JavaScript

---

# Project Structure

```text
MediaHub-Desktop/
│
├── app.py
├── downloads/
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
├── README.md
└── requirements.txt
```

---

# Installation


## 1. Install Python Dependencies

```bash
pip install flask yt-dlp
```

---

## 2. Install FFmpeg

Download FFmpeg from:

https://www.gyan.dev/ffmpeg/builds/

Extract it and add the `bin` folder to your system PATH.

Verify installation:

```bash
ffmpeg -version
```

---

# Running the Application

```bash
python app.py
```

Open browser:

```text
http://127.0.0.1:5000
```

---

# How to Use

## Single Video
1. Paste video link
2. Click Fetch
3. Select quality
4. Choose MP3 option if needed
5. Click Download

## Playlist
1. Paste playlist link
2. Click Fetch
3. Select desired videos
4. Choose quality/audio option
5. Click Download

---

# Known Limitations

- Playlist downloads use shared quality settings
- Some protected or restricted videos may not download
- Exact file size may not always be available from source platforms

---

