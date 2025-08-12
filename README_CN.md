# pip下载加速配置（Pip Mirror Manager）

跨平台的 pip 镜像切换器。内置多家稳定 HTTPS 镜像，支持自定义；自动识别语言（简体/繁體/英文），提供 Tk GUI 与 CLI 回退；按规范写入用户级配置，若选择 HTTP 源会自动加入 trusted-host。

主要特性
- 一键切换 pip 下载源（index-url）
- 内置镜像（均为 HTTPS）：官方、清华 TUNA、BFSU、SJTU、USTC、ZJU、阿里云、华为云、腾讯云
- 支持自定义镜像 URL
- 自动语言：简体/繁体/英文（其余默认英文）；可 --lang 强制
- GUI 友好界面，大小可调整；无图形环境自动回退到命令行
- 按平台写入用户级配置：安全、无需管理员权限
- 选择 HTTP 源时自动写入 trusted-host（便于证书校验通过）

环境要求
- Windows / macOS / Linux
- Python 3.6 及以上（不支持 Python 2）

快速开始
1) 克隆仓库或下载单文件脚本（假设文件名为 pip_mirror_manager.py）
2) 运行
   - GUI：python pip_mirror_manager.py
   - CLI：python pip_mirror_manager.py --cli
   - 强制语言：python pip_mirror_manager.py --lang=zh_Hant  或  --lang=zh_Hans / --lang=en

命令行用法（示例）
- 列表中选择镜像：输入序号
- 使用自定义 URL：输入 0 并粘贴 http/https 地址
- 恢复官方源：输入 R
- 退出：输入 Q

内置镜像
- 官方 PyPI：https://pypi.org/simple/
- 清华 TUNA：https://pypi.tuna.tsinghua.edu.cn/simple/
- 北京外国语大学 BFSU：https://mirrors.bfsu.edu.cn/pypi/web/simple/
- 上海交通大学 SJTU：https://mirror.sjtu.edu.cn/pypi/web/simple/
- 中国科学技术大学 USTC：https://mirrors.ustc.edu.cn/pypi/web/simple/
- 浙江大学 ZJU：https://mirrors.zju.edu.cn/pypi/web/simple/
- 阿里云：https://mirrors.aliyun.com/pypi/simple/
- 华为云：https://mirrors.huaweicloud.com/repository/pypi/simple/
- 腾讯云：https://mirrors.cloud.tencent.com/pypi/simple/
- 注：豆瓣长期不稳定，未默认收录；可自行添加为自定义源

配置文件位置（用户级）
- Windows：%APPDATA%\pip\pip.ini
- macOS：~/Library/Application Support/pip/pip.conf
- Linux：~/.config/pip/pip.conf（兼容旧路径 ~/.pip/pip.conf）
- 程序会自动创建目录与文件；HTTP 源会写入 trusted-host

常见问题
- 证书相关错误：优先使用 HTTPS 镜像；若必须使用 HTTP，程序会自动添加 trusted-host
- 管理员权限：用户级配置不需要管理员；若要全局配置，请另行以管理员身份写入系统级配置（可在后续版本中加入选项）
- 高 DPI：Windows 下自动启用 DPI 感知，界面更清晰

打包为可执行文件（可选）
- 使用 PyInstaller：pyinstaller -F -w pip_mirror_manager.py
  - -F 单文件；-w 隐藏控制台（GUI）

贡献
- 欢迎提 Issue/PR：新增镜像、改进界面、完善文档与本地化

许可
- 建议使用 MIT 许可（可按项目需要更改）
