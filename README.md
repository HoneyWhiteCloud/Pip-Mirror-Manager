# Pip Mirror Manager (pip下载加速配置)

A cross‑platform PyPI mirror switcher for pip. Ships with popular HTTPS mirrors and custom URL support; auto language detection (zh‑Hans/zh‑Hant/en), Tk GUI with CLI fallback; writes user‑level config per platform and adds trusted‑host when using HTTP.

Features
- One‑click switch of pip index‑url
- Built‑in HTTPS mirrors: Official, Tsinghua TUNA, BFSU, SJTU, USTC, ZJU, Aliyun, Huawei Cloud, Tencent Cloud
- Custom mirror URL support
- Auto language: Simplified/Traditional Chinese and English (others default to English); optional --lang override
- Friendly Tk GUI; resizable window; automatic CLI fallback in headless environments
- Writes user‑level config (no admin rights)
- Automatically adds trusted‑host for HTTP mirrors

Requirements
- Windows / macOS / Linux
- Python 3.6+

Quick Start
1) Clone the repo or download the single Python file (assume pip_mirror_manager.py)
2) Run
   - GUI: python pip_mirror_manager.py
   - CLI: python pip_mirror_manager.py --cli
   - Force language: python pip_mirror_manager.py --lang=zh_Hant (or zh_Hans / en)

CLI usage (examples)
- Pick a mirror by number
- Use a custom URL: enter 0, then paste an http/https URL
- Restore official source: enter R
- Quit: enter Q

Built‑in mirrors
- Official PyPI: https://pypi.org/simple/
- Tsinghua TUNA: https://pypi.tuna.tsinghua.edu.cn/simple/
- BFSU: https://mirrors.bfsu.edu.cn/pypi/web/simple/
- SJTU: https://mirror.sjtu.edu.cn/pypi/web/simple/
- USTC: https://mirrors.ustc.edu.cn/pypi/web/simple/
- ZJU: https://mirrors.zju.edu.cn/pypi/web/simple/
- Aliyun: https://mirrors.aliyun.com/pypi/simple/
- Huawei Cloud: https://mirrors.huaweicloud.com/repository/pypi/simple/
- Tencent Cloud: https://mirrors.cloud.tencent.com/pypi/simple/
- Note: Douban is often unstable and not included by default; add it as a custom URL if needed

Config locations (user‑level)
- Windows: %APPDATA%\pip\pip.ini
- macOS: ~/Library/Application Support/pip/pip.conf
- Linux: ~/.config/pip/pip.conf (legacy ~/.pip/pip.conf supported)
- The app creates folders/files automatically; trusted-host is written for HTTP sources

FAQ
- TLS/certificate errors: prefer HTTPS mirrors; for HTTP the app adds trusted‑host automatically
- Admin rights: not needed for user‑level config. For system‑wide config, write to the system path with elevated privileges (could be added as an option later)
- High DPI: DPI awareness is enabled on Windows for crisper UI

Packaging to an executable (optional)
- PyInstaller: pyinstaller -F -w pip_mirror_manager.py
  - -F single file, -w windowed (hide console for GUI)

Contributing
- Issues and PRs are welcome: new mirrors, UI improvements, docs and localization

License
- MIT is recommended (adjust as needed)
