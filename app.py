from flask import Flask, render_template, request, jsonify
import yt_dlp
import os
import threading

app = Flask(__name__)

# =========================
# CREATE DOWNLOAD FOLDER
# =========================

DOWNLOAD_FOLDER = "downloads"

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# =========================
# GLOBAL PROGRESS DATA
# =========================

progress_data = {
    "percent": "0%",
    "speed": "0 KB/s",
    "eta": "0 sec",
    "current": "",
    "status": "idle"
}

# =========================
# CANCEL FLAG
# =========================

stop_flag = {
    "stop": False
}

# =========================
# DOWNLOAD TASK
# =========================

def download_task(data):

    def hook(d):

        # CANCEL DOWNLOAD
        if stop_flag["stop"]:
            raise Exception("Download cancelled")

        # UPDATE PROGRESS
        if d['status'] == 'downloading':

            progress_data["percent"] = (
                d.get('_percent_str', '0%').strip()
            )

            progress_data["speed"] = (
                d.get('_speed_str', '0 KB/s')
            )

            progress_data["eta"] = (
                d.get('_eta_str', '0 sec')
            )

            progress_data["current"] = (
                d.get('filename', '')
            )

            progress_data["status"] = "downloading"

    # =========================
    # YT-DLP OPTIONS
    # =========================

    ydl_opts = {
        "outtmpl":
            f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",

        "progress_hooks":
            [hook]
    }

    try:

        # =========================
        # PLAYLIST DOWNLOAD
        # =========================

        if data.get("urls"):

            urls = data["urls"]

            quality = data.get(
                "quality",
                "best"
            )

            is_audio = data.get(
                "audio",
                False
            )

            # MP3 DOWNLOAD
            if is_audio:

                ydl_opts.update({
                    "format":
                        "bestaudio/best",

                    "postprocessors": [{
                        "key":
                            "FFmpegExtractAudio",

                        "preferredcodec":
                            "mp3",
                    }]
                })

            # VIDEO DOWNLOAD
            else:
                ydl_opts["format"] = quality

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download(urls)

        # =========================
        # SINGLE VIDEO DOWNLOAD
        # =========================

        else:

            url = data["url"]

            format_id = data.get("format_id")

            is_audio = data.get("audio")

            # MP3 DOWNLOAD
            if is_audio:

                ydl_opts.update({
                    "format":
                        "bestaudio/best",

                    "postprocessors": [{
                        "key":
                            "FFmpegExtractAudio",

                        "preferredcodec":
                            "mp3",
                    }]
                })

            # VIDEO DOWNLOAD
            else:
                ydl_opts["format"] = format_id

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        progress_data["status"] = "completed"

    except Exception as e:

        print("DOWNLOAD ERROR:", str(e))

        progress_data["status"] = "cancelled"

    progress_data["percent"] = "0%"

    stop_flag["stop"] = False


# =========================
# DOWNLOAD ROUTE
# =========================

@app.route("/download", methods=["POST"])
def download():

    data = request.json

    stop_flag["stop"] = False

    progress_data["status"] = "starting"

    threading.Thread(
        target=download_task,
        args=(data,)
    ).start()

    return {
        "status": "started"
    }


# =========================
# CANCEL ROUTE
# =========================

@app.route("/cancel", methods=["POST"])
def cancel():

    stop_flag["stop"] = True

    return {
        "status": "cancelling"
    }


# =========================
# PROGRESS ROUTE
# =========================

@app.route("/progress")
def progress():

    return jsonify(progress_data)


# =========================
# VIDEO / PLAYLIST INFO
# =========================

@app.route("/info", methods=["POST"])
def get_info():

    try:

        url = request.json["url"]

        ydl_opts = {
            "quiet": True,
            "noplaylist": False
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(
                url,
                download=False
            )

        # =========================
        # PLAYLIST
        # =========================

        if "entries" in info:

            videos = []

            for v in info["entries"]:

                if v:

                    videos.append({
                        "title":
                            v["title"],

                        "url":
                            f"https://www.youtube.com/watch?v={v['id']}",

                        "thumbnail":
                            f"https://img.youtube.com/vi/{v['id']}/hqdefault.jpg"
                    })

            return jsonify({
                "type": "playlist",
                "videos": videos
            })

        # =========================
        # SINGLE VIDEO
        # =========================

        formats = []

        for f in info["formats"]:

            size = (
                f.get("filesize")
                or
                f.get("filesize_approx")
            )

            if size:
                size = round(
                    size / (1024 * 1024),
                    2
                )
            else:
                size = "N/A"

            formats.append({
                "format_id":
                    f["format_id"],

                "ext":
                    f["ext"],

                "quality":
                    f.get(
                        "format_note",
                        "unknown"
                    ),

                "filesize":
                    size
            })

        return jsonify({
            "type":
                "video",

            "title":
                info["title"],

            "thumbnail":
                info["thumbnail"],

            "formats":
                formats[:15]
        })

    except Exception as e:

        print("INFO ERROR:", str(e))

        return jsonify({
            "error": str(e)
        }), 500


# =========================
# HOME PAGE
# =========================

@app.route("/")
def index():

    return render_template("index.html")


# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    app.run()