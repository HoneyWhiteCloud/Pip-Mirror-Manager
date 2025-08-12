#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import locale
import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

import configparser
from urllib.parse import urlparse

# ================== 语言检测（避免使用已弃用的 getdefaultlocale） ==================
def detect_language():
    """
    返回 'zh_Hans'（简体）/ 'zh_Hant'（繁體）/ 'en'（默认）
    检测优先级：
      1) 环境变量 LC_ALL / LC_MESSAGES / LANG
      2) Windows: GetUserDefaultUILanguage -> locale.windows_locale
      3) locale.getlocale() 回退
    支持通过 --lang 覆盖。
    """
    # 命令行覆盖
    for i, arg in enumerate(sys.argv[1:]):
        if arg.startswith("--lang="):
            forced = arg.split("=", 1)[1].strip()
            if forced in ("en", "zh_Hans", "zh_Hant"):
                return forced
        if arg == "--lang" and i + 2 < len(sys.argv):
            forced = sys.argv[i + 2]
            if forced in ("en", "zh_Hans", "zh_Hant"):
                return forced

    # 1) 环境变量
    cand = (
        os.environ.get("LC_ALL")
        or os.environ.get("LC_MESSAGES")
        or os.environ.get("LANG")
        or ""
    )
    cand = (cand or "").replace("-", "_").lower()

    # 2) Windows UI 语言
    if not cand and os.name == "nt":
        try:
            import ctypes
            langid = ctypes.windll.kernel32.GetUserDefaultUILanguage()
            code = locale.windows_locale.get(langid, "")
            cand = (code or "").replace("-", "_").lower()
        except Exception:
            pass

    # 3) 回退到 locale.getlocale（未弃用）
    if not cand:
        try:
            code = (locale.getlocale()[0] or "")
            cand = code.replace("-", "_").lower()
        except Exception:
            cand = ""

    def is_hans(code):
        return any(code.startswith(x) for x in ("zh_cn", "zh_sg", "zh_hans"))

    def is_hant(code):
        return any(code.startswith(x) for x in ("zh_tw", "zh_hk", "zh_mo", "zh_hant"))

    if cand.startswith("zh"):
        return "zh_Hant" if is_hant(cand) else "zh_Hans"
    return "en"


LANG = detect_language()

# 你可在此自定义英文应用名称
EN_APP_NAME = "Pip Mirror Manager"

# ================== 多语言字典 ==================
TRANSLATIONS = {
    "en": {
        "app.title": EN_APP_NAME,
        "label.user_config_file": "User config file:",
        "btn.open_folder": "Open Folder",
        "group.select_mirror": "Select Mirror",
        "label.common_mirrors": "Common mirrors:",
        "label.custom_url": "Custom URL:",
        "btn.save_user": "Save (user config)",
        "btn.restore_official": "Restore Official",
        "btn.exit": "Exit",
        "status.current_index": "Current index-url: {url}",
        "tip": "Tip: Prefer HTTPS mirrors; if you choose HTTP, trusted-host will be added automatically.\n"
               "User-level config affects only the current user and needs no administrator rights.",
        "error": "Error",
        "error.open_folder": "Cannot open folder:\n{err}",
        "warn.invalid_url_title": "Invalid URL",
        "warn.invalid_url_msg": "Please enter a valid http/https URL.",
        "ok.title": "Success",
        "ok.saved": "pip index-url is set to:\n{url}\n\nFile: {path}",
        "fail.write_title": "Write Failed",
        "fail.write_msg": "Failed to write config:\n{err}",
        "ok.restored_title": "Restored",
        "ok.restored_msg": "Restored to official source (https://pypi.org/simple/).",
        "fail.restore_title": "Operation Failed",
        "fail.restore_msg": "Restore failed:\n{err}",
        "custom": "Custom",
        "loaded": "(Loaded)",
        "cli.title": "Pip Mirror Manager (CLI)",
        "cli.menu": "Choose a mirror (number) or 0 for custom URL, R to restore official, Q to quit:",
        "cli.prompt": "Your choice: ",
        "cli.enter_custom": "Enter custom URL (http/https): ",
        "cli.invalid": "Invalid input. Try again.",
        "cli.saved": "Saved. Config file: {path}\nindex-url = {url}",
        "cli.restored": "Restored to official source.",
        "cli.invalid_url": "Invalid URL.",
        "cli.enter_to_exit": "Press Enter to exit...",
        # Mirrors
        "mirror.official": "Official PyPI",
        "mirror.tuna": "Tsinghua TUNA",
        "mirror.bfsu": "BFSU",
        "mirror.sjtu": "SJTU",
        "mirror.ustc": "USTC",
        "mirror.zju": "ZJU",
        "mirror.aliyun": "Aliyun",
        "mirror.huawei": "Huawei Cloud",
        "mirror.tencent": "Tencent Cloud",
        # "mirror.douban": "Douban (unstable)",
    },
    "zh_Hans": {
        "app.title": "pip下载加速配置",
        "label.user_config_file": "用户配置文件：",
        "btn.open_folder": "打开文件夹",
        "group.select_mirror": "选择镜像",
        "label.common_mirrors": "常用镜像：",
        "label.custom_url": "自定义 URL：",
        "btn.save_user": "保存为用户配置",
        "btn.restore_official": "恢复官方源",
        "btn.exit": "退出",
        "status.current_index": "当前 index-url：{url}",
        "tip": "提示：优先推荐使用 HTTPS 镜像；如果选择 HTTP，将自动写入 trusted-host。\n"
               "用户级配置仅影响当前用户，无需管理员权限。",
        "error": "错误",
        "error.open_folder": "无法打开文件夹：\n{err}",
        "warn.invalid_url_title": "无效的 URL",
        "warn.invalid_url_msg": "请输入正确的 http/https 地址。",
        "ok.title": "成功",
        "ok.saved": "pip 下载源已配置为：\n{url}\n\n文件：{path}",
        "fail.write_title": "写入失败",
        "fail.write_msg": "写入配置失败：\n{err}",
        "ok.restored_title": "已恢复",
        "ok.restored_msg": "已恢复为官方源（https://pypi.org/simple/）。",
        "fail.restore_title": "操作失败",
        "fail.restore_msg": "恢复失败：\n{err}",
        "custom": "自定义",
        "loaded": "（已加载）",
        "cli.title": "pip下载加速配置（命令行）",
        "cli.menu": "选择镜像（输入序号），或输入 0 使用自定义 URL，输入 R 恢复官方源，输入 Q 退出：",
        "cli.prompt": "请输入：",
        "cli.enter_custom": "请输入自定义 URL（http/https）：",
        "cli.invalid": "输入无效，请重试。",
        "cli.saved": "已保存。配置文件：{path}\nindex-url = {url}",
        "cli.restored": "已恢复为官方源。",
        "cli.invalid_url": "URL 无效。",
        "cli.enter_to_exit": "按回车键退出……",
        # Mirrors
        "mirror.official": "官方 PyPI",
        "mirror.tuna": "清华大学 TUNA",
        "mirror.bfsu": "北京外国语大学 BFSU",
        "mirror.sjtu": "上海交通大学 SJTU",
        "mirror.ustc": "中国科学技术大学 USTC",
        "mirror.zju": "浙江大学 ZJU",
        "mirror.aliyun": "阿里云",
        "mirror.huawei": "华为云",
        "mirror.tencent": "腾讯云",
        # "mirror.douban": "豆瓣（不稳定）",
    },
    "zh_Hant": {
        "app.title": "pip下載加速配置",
        "label.user_config_file": "使用者設定檔：",
        "btn.open_folder": "開啟資料夾",
        "group.select_mirror": "選擇鏡像",
        "label.common_mirrors": "常用鏡像：",
        "label.custom_url": "自訂 URL：",
        "btn.save_user": "儲存為使用者設定",
        "btn.restore_official": "恢復官方來源",
        "btn.exit": "離開",
        "status.current_index": "目前 index-url：{url}",
        "tip": "提示：建議優先使用 HTTPS 鏡像；若選擇 HTTP，將自動寫入 trusted-host。\n"
               "使用者層級設定僅影響目前使用者，無需系統管理員權限。",
        "error": "錯誤",
        "error.open_folder": "無法開啟資料夾：\n{err}",
        "warn.invalid_url_title": "無效的 URL",
        "warn.invalid_url_msg": "請輸入正確的 http/https 位址。",
        "ok.title": "成功",
        "ok.saved": "已將 pip 下載源設定為：\n{url}\n\n檔案：{path}",
        "fail.write_title": "寫入失敗",
        "fail.write_msg": "寫入設定失敗：\n{err}",
        "ok.restored_title": "已恢復",
        "ok.restored_msg": "已恢復為官方來源（https://pypi.org/simple/）。",
        "fail.restore_title": "操作失敗",
        "fail.restore_msg": "恢復失敗：\n{err}",
        "custom": "自訂",
        "loaded": "（已載入）",
        "cli.title": "pip下載加速配置（命令列）",
        "cli.menu": "選擇鏡像（輸入序號），或輸入 0 使用自訂 URL，輸入 R 恢復官方來源，輸入 Q 離開：",
        "cli.prompt": "請輸入：",
        "cli.enter_custom": "請輸入自訂 URL（http/https）：",
        "cli.invalid": "輸入無效，請重試。",
        "cli.saved": "已儲存。設定檔：{path}\nindex-url = {url}",
        "cli.restored": "已恢復為官方來源。",
        "cli.invalid_url": "URL 無效。",
        "cli.enter_to_exit": "按下 Enter 鍵離開……",
        # Mirrors
        "mirror.official": "官方 PyPI",
        "mirror.tuna": "清華大學 TUNA",
        "mirror.bfsu": "北京外國語大學 BFSU",
        "mirror.sjtu": "上海交通大學 SJTU",
        "mirror.ustc": "中國科學技術大學 USTC",
        "mirror.zju": "浙江大學 ZJU",
        "mirror.aliyun": "阿里雲",
        "mirror.huawei": "華為雲",
        "mirror.tencent": "騰訊雲",
        # "mirror.douban": "豆瓣（不穩定）",
    },
}

def t(key, **kwargs):
    base = TRANSLATIONS.get("en", {})
    data = TRANSLATIONS.get(LANG, base)
    text = data.get(key, base.get(key, key))
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text

# ================== 镜像源（尽量使用 https） ==================
MIRROR_DEFS = [
    ("official", "https://pypi.org/simple/"),
    ("tuna",     "https://pypi.tuna.tsinghua.edu.cn/simple/"),
    ("bfsu",     "https://mirrors.bfsu.edu.cn/pypi/web/simple/"),
    ("sjtu",     "https://mirror.sjtu.edu.cn/pypi/web/simple/"),
    ("ustc",     "https://mirrors.ustc.edu.cn/pypi/web/simple/"),
    ("zju",      "https://mirrors.zju.edu.cn/pypi/web/simple/"),
    ("aliyun",   "https://mirrors.aliyun.com/pypi/simple/"),
    ("huawei",   "https://mirrors.huaweicloud.com/repository/pypi/simple/"),
    ("tencent",  "https://mirrors.cloud.tencent.com/pypi/simple/"),
    # 豆瓣長期不穩定，如需可取消註釋
    # ("douban",   "https://pypi.doubanio.com/simple/"),
]

DEFAULT_URL = MIRROR_DEFS[0][1]

# ================== 配置文件路径（跨平台） ==================
def get_user_pip_config_path():
    """
    返回用户级 pip 配置文件路径（跨平台）：
    - Windows: %APPDATA%\\pip\\pip.ini
    - macOS:   ~/Library/Application Support/pip/pip.conf
    - Linux:   ~/.config/pip/pip.conf ；若不存在则回退 ~/.pip/pip.conf
    """
    if os.name == "nt":
        appdata = os.environ.get("APPDATA") or str(Path.home() / "AppData" / "Roaming")
        pip_dir = Path(appdata) / "pip"
        suffix = "pip.ini"
    elif sys.platform == "darwin":
        pip_dir = Path.home() / "Library" / "Application Support" / "pip"
        suffix = "pip.conf"
    else:
        # POSIX
        pip_dir = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "pip"
        suffix = "pip.conf"
        # 兼容旧路径 ~/.pip/pip.conf
        legacy = Path.home() / ".pip" / "pip.conf"
        if legacy.exists() and not (pip_dir / suffix).exists():
            pip_dir = legacy.parent
    pip_dir.mkdir(parents=True, exist_ok=True)
    return pip_dir / suffix

# ================== 读写配置 ==================
def read_current_index_url(cfg_path):
    """
    读取现有配置中的 index-url（若无则返回空字符串）
    """
    path = Path(cfg_path)
    if not path.exists():
        return ""
    cp = configparser.RawConfigParser()
    # 尝试多种编码
    for enc in ("utf-8", "utf-8-sig", "mbcs", "latin-1"):
        try:
            cp.read(path, encoding=enc)
            break
        except Exception:
            continue
    if cp.has_section("global") and cp.has_option("global", "index-url"):
        return cp.get("global", "index-url").strip()
    return ""

def write_pip_config(cfg_path, index_url):
    """
    写入 [global] index-url；若是 http 则自动加入 trusted-host
    """
    path = Path(cfg_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    host = urlparse(index_url).hostname or ""
    lines = ["[global]", "index-url = {0}".format(index_url)]
    if index_url.lower().startswith("http://") and host:
        lines.append("trusted-host = {0}".format(host))
    content = "\n".join(lines) + "\n"
    # 使用 utf-8 写入
    with path.open("w", encoding="utf-8") as f:
        f.write(content)

def is_valid_url(url):
    try:
        u = urlparse(url)
        return u.scheme in ("http", "https") and bool(u.netloc)
    except Exception:
        return False

# ================== GUI ==================
class PipMirrorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(t("app.title"))
        self.resizable(True, True)

        self.cfg_path = get_user_pip_config_path()
        self.current_url = read_current_index_url(self.cfg_path) or DEFAULT_URL

        self._build_widgets()
        self._load_current_selection()
        self._apply_layout_policies()
        self.bind("<Configure>", self._on_resize)

    def _build_widgets(self):
        padding = {"padx": 12, "pady": 8}

        # 顶部：路径与打开按钮
        frm_top = ttk.Frame(self)
        frm_top.pack(fill="x", **padding)

        ttk.Label(frm_top, text=t("label.user_config_file")).pack(side="left")
        self.lbl_path = ttk.Label(frm_top, text=str(self.cfg_path), foreground="#555")
        self.lbl_path.pack(side="left", fill="x", expand=True)

        btn_open = ttk.Button(frm_top, text=t("btn.open_folder"), command=self.open_folder)
        btn_open.pack(side="right")

        # 中部：镜像选择 + 自定义
        frm_mid = ttk.LabelFrame(self, text=t("group.select_mirror"))
        frm_mid.pack(fill="x", **padding)

        ttk.Label(frm_mid, text=t("label.common_mirrors")).grid(row=0, column=0, sticky="w", padx=8, pady=6)

        mirror_values = [u"{0}  |  {1}".format(t("mirror." + mid), url) for mid, url in MIRROR_DEFS]

        self.combo = ttk.Combobox(frm_mid, state="readonly", values=mirror_values)
        self.combo.grid(row=0, column=1, sticky="ew", padx=8, pady=6)
        frm_mid.columnconfigure(1, weight=1)

        ttk.Label(frm_mid, text=t("label.custom_url")).grid(row=1, column=0, sticky="w", padx=8, pady=6)
        self.ent_custom = ttk.Entry(frm_mid)
        self.ent_custom.grid(row=1, column=1, sticky="ew", padx=8, pady=6)

        # 主操作按钮
        frm_primary = ttk.Frame(self)
        frm_primary.pack(fill="x", **padding)
        self.btn_save = ttk.Button(frm_primary, text=t("btn.save_user"), command=self.save_config)
        self.btn_save.pack(side="left")

        # 次要按钮
        frm_btn = ttk.Frame(self)
        frm_btn.pack(fill="x", **padding)
        ttk.Button(frm_btn, text=t("btn.restore_official"), command=self.restore_default).pack(side="left")
        ttk.Button(frm_btn, text=t("btn.exit"), command=self.quit).pack(side="right")

        # 当前状态
        frm_status = ttk.Frame(self)
        frm_status.pack(fill="x", **padding)
        self.status_var = tk.StringVar(value="")
        ttk.Label(frm_status, textvariable=self.status_var, foreground="#0a7").pack(anchor="w")

        # 底部提示（自动换行）
        self.lbl_tip = ttk.Label(self, text=t("tip"), foreground="#666", justify="left")
        self.lbl_tip.pack(anchor="w", fill="x", padx=12, pady=(0, 12))

    def _load_current_selection(self):
        current = self.current_url.strip().rstrip("/")
        matched = False
        for idx, (_, url) in enumerate(MIRROR_DEFS):
            if current == url.strip().rstrip("/"):
                self.combo.current(idx)
                matched = True
                break
        if not matched:
            self.combo.set(u"{0}  |  {1}".format(t("custom"), t("loaded")))
            self.ent_custom.delete(0, tk.END)
            self.ent_custom.insert(0, self.current_url)
        self.status_var.set(t("status.current_index", url=self.current_url))

    def _apply_layout_policies(self):
        self.update_idletasks()
        self._update_tip_wraplength()
        req_w = self.winfo_reqwidth()
        req_h = self.winfo_reqheight()
        # 设为最小尺寸以避免裁切
        self.minsize(req_w, req_h)
        self._center_window(req_w, req_h)

    def _update_tip_wraplength(self):
        width = max(self.winfo_width(), self.winfo_reqwidth())
        wrap = max(200, width - 24)
        try:
            self.lbl_tip.configure(wraplength=wrap)
        except Exception:
            pass

    def _center_window(self, w=None, h=None):
        self.update_idletasks()
        if w is None:
            w = self.winfo_width()
        if h is None:
            h = self.winfo_height()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = int((sw - w) / 2)
        y = int((sh - h) / 2.5)
        self.geometry("{0}x{1}+{2}+{3}".format(w, h, x, y))

    def _on_resize(self, event):
        self._update_tip_wraplength()

    def open_folder(self):
        folder = str(Path(self.cfg_path).parent)
        try:
            if os.name == "nt":
                os.startfile(folder)
            elif sys.platform == "darwin":
                subprocess.run(["open", folder], check=False)
            else:
                subprocess.run(["xdg-open", folder], check=False)
        except Exception as e:
            messagebox.showerror(t("error"), t("error.open_folder", err=e))

    def get_target_url(self):
        custom = self.ent_custom.get().strip()
        if custom:
            return custom
        sel = self.combo.get()
        if " | " in sel:
            return sel.split(" | ")[-1].strip()
        return DEFAULT_URL

    def save_config(self):
        url = self.get_target_url()
        if not is_valid_url(url):
            messagebox.showwarning(t("warn.invalid_url_title"), t("warn.invalid_url_msg"))
            return
        try:
            write_pip_config(self.cfg_path, url)
            self.current_url = url
            self.status_var.set(t("status.current_index", url=url))
            messagebox.showinfo(t("ok.title"), t("ok.saved", url=url, path=self.cfg_path))
        except Exception as e:
            messagebox.showerror(t("fail.write_title"), t("fail.write_msg", err=e))

    def restore_default(self):
        try:
            write_pip_config(self.cfg_path, DEFAULT_URL)
            self.current_url = DEFAULT_URL
            self.ent_custom.delete(0, tk.END)
            for idx, (_, url) in enumerate(MIRROR_DEFS):
                if url.strip().rstrip("/") == DEFAULT_URL.strip().rstrip("/"):
                    self.combo.current(idx)
                    break
            self.status_var.set(t("status.current_index", url=DEFAULT_URL))
            messagebox.showinfo(t("ok.restored_title"), t("ok.restored_msg"))
        except Exception as e:
            messagebox.showerror(t("fail.restore_title"), t("fail.restore_msg", err=e))

# ================== CLI 回退（可选） ==================
def run_cli():
    cfg_path = get_user_pip_config_path()
    current = read_current_index_url(cfg_path) or DEFAULT_URL
    print(t("cli.title"))
    print("-" * 60)
    print(t("status.current_index", url=current))
    print()
    for i, (mid, url) in enumerate(MIRROR_DEFS, 1):
        print("{0}. {1}: {2}".format(i, t("mirror." + mid), url))
    print("0. {0}".format(t("custom")))
    print("R. {0}".format(t("btn.restore_official")))
    print("Q. quit")
    while True:
        try:
            print()
            print(t("cli.menu"))
            choice = input(t("cli.prompt")).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not choice:
            print(t("cli.invalid"))
            continue
        if choice.lower() == "q":
            break
        if choice.lower() == "r":
            try:
                write_pip_config(cfg_path, DEFAULT_URL)
                print(t("cli.restored"))
            except Exception as e:
                print(t("fail.restore_msg", err=e))
            continue
        if choice == "0":
            url = input(t("cli.enter_custom")).strip()
            if not is_valid_url(url):
                print(t("cli.invalid_url"))
                continue
            try:
                write_pip_config(cfg_path, url)
                print(t("cli.saved", path=cfg_path, url=url))
            except Exception as e:
                print(t("fail.write_msg", err=e))
            continue
        # 数字镜像
        try:
            idx = int(choice)
            if not (1 <= idx <= len(MIRROR_DEFS)):
                print(t("cli.invalid"))
                continue
            url = MIRROR_DEFS[idx - 1][1]
            write_pip_config(cfg_path, url)
            print(t("cli.saved", path=cfg_path, url=url))
        except ValueError:
            print(t("cli.invalid"))
        except Exception as e:
            print(t("fail.write_msg", err=e))
    # Windows 控制台停留
    if os.name == "nt":
        try:
            input(t("cli.enter_to_exit"))
        except Exception:
            pass

# ================== 入口 ==================
def main():
    # 命令行参数：--cli 强制命令行模式
    if "--cli" in sys.argv:
        run_cli()
        return

    # 高 DPI（Windows）
    if os.name == "nt":
        try:
            import ctypes
            try:
                ctypes.windll.shcore.SetProcessDpiAwareness(1)
            except Exception:
                ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

    # 启动 GUI；若 Tk 不可用则回退到 CLI
    try:
        app = PipMirrorGUI()
        app.mainloop()
    except tk.TclError:
        run_cli()

if __name__ == "__main__":
    main()