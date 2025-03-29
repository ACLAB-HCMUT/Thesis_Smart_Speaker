#!/bin/bash

sudo systemctl restart snapclient

if [ -z "$1" ]; then
    echo "Usage: $0 'Song Name'"
    exit 1
fi

# Tìm kiếm video trên YouTube và lấy link của kết quả đầu tiên
URL=$(yt-dlp -f bestaudio --extractor-args "youtube:formats=missing_pot" --get-url "ytsearch1:$1")

if [ -z "$URL" ]; then
    echo "Không thể tìm thấy URL cho bài hát: $1"
    exit 1
fi

echo "Đang phát: $1 ($URL)"

# Phát trực tiếp âm thanh vào Snapcast
yt-dlp -f bestaudio --extractor-args "youtube:formats=missing_pot" "$URL" -o - | ffmpeg -i pipe:0 -f wav -ar 48000 -ac 2 -acodec pcm_s16le - > /tmp/snapfifo
