# Yandex Music to CSV Exporter 🎵

A lightweight, asynchronous Python CLI tool to export your liked tracks from Yandex Music into a universal CSV format. 

Perfect for users migrating to international streaming platforms like **Spotify**, **Apple Music**, or **YouTube Music**. Since official cross-platform sync APIs are often restricted, this script handles data extraction and prepares a structured file compatible with free migration services (e.g., TuneMyMusic or Soundiiz).

## ✨ Features
* 🚀 **Fully Asynchronous:** Powered by `yandex-music` API for fast data fetching.
* 💻 **Modern CLI Interface:** Clean and beautiful terminal UI built with `typer` and `rich`.
* 🛡 **Secure Storage:** Your personal tokens are kept safe locally in a `.env` file.
* 📊 **Progress Tracking:** Interactive progress bars during data export.

## 🛠 Installation & Usage

1. Clone the repository and install dependencies:
```bash
git clone [https://github.com/Nikita261012/YMParser.git](https://github.com/Nikita261012/YMParser.git)
cd YMParser
pip install -r requirements.txt
