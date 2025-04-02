#!/bin/bash
# sudo systemctl restart snapclient
# Thay YOUR_YOUTUBE_API_KEY bằng API Key của bạn
sudo sed -i "s/^SNAPCLIENT_OPTS=.*/SNAPCLIENT_OPTS=\"--host=127.0.0.1 --soundcard hw:USB,0 \"/" /etc/default/snapclient
sudo systemctl restart snapclient
API_KEY="AIzaSyAdzkBaTsl5s4xwZHQuevX9YgMh-Miwj9o"
FIFO_PATH="/tmp/snapfifo"

if [ -z "$1" ]; then
    echo "Usage: $0 'Tên bài hát'"
    exit 1
fi

if [ ! -p "$FIFO_PATH" ]; then
    echo "❌ Không tìm thấy $FIFO_PATH. Kiểm tra Snapserver!"
    exit 1
fi


# Tìm kiếm video trên YouTube API
echo "🔍 Tìm kiếm bài hát: $1"
API_URL="https://www.googleapis.com/youtube/v3/search?part=snippet&q=${1// /+}&type=video&key=$API_KEY"
VIDEO_ID=$(curl -s "$API_URL" | jq -r '.items[0].id.videoId')

    if [ -z "$VIDEO_ID" ] || [ "$VIDEO_ID" == "null" ]; then
        echo "❌ Không tìm thấy bài hát: $1"
        exit 1
    fi

    URL="https://www.youtube.com/watch?v=$VIDEO_ID"
    echo "🎵 Đang phát: $1 ($URL)"

    # Lấy link audio bằng yt-dlp
    AUDIO_URL=$(yt-dlp -f bestaudio --get-url "$URL")

    if [ -z "$AUDIO_URL" ]; then
        echo "❌ Không lấy được link audio."
        exit 1
    fi


# Phát nhạc vào Snapserver bằng mpv
mpv "$AUDIO_URL" --no-video --audio-display=no --audio-channels=stereo \
    --audio-samplerate=48000 --audio-format=s16 --ao=pcm --ao-pcm-file="$FIFO_PATH" \
    --input-ipc-server=/tmp/mpv_socket
