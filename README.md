# UNM Sport Booking Helper

这个项目用于打开 University of Nottingham Malaysia 的 Sport Complex booking 页面，并通过 Playwright 自动填写部分预订流程。

当前脚本会：

- 打开 sport complex booking 页面
- 如遇到登录页，使用 `.env` 里的账号密码登录
- 打开 `Other Facilities Online`
- 进入 `Booking Request` -> `New Booking`
- 在 GUI 里选择账号、场地、日期、时间和用途
- 填写 email、contact number、purpose
- 选择 badminton court 和 sport type
- 最后根据 `Auto click Complete` 的选择决定是否自动点击 `Complete`

请只使用自己的学校账号，并遵守学校场地预订规则。

## 文件说明

- `main.py`：主程序
- `requirements.txt`：Python 依赖列表
- `.env.example`：账号配置模板
- `.env`：你自己的真实账号配置，本地创建，不要提交到 Git
- `picklocator.txt`：开发时记录过的页面定位信息

## Windows 从零开始运行

1. 安装 Python

   下载并安装 Python 3.11 或更新版本：

   ```text
   https://www.python.org/downloads/
   ```

   安装时建议勾选：

   ```text
   Add python.exe to PATH
   ```

2. 打开项目文件夹

   在 `D:\1\booking` 文件夹空白处右键，选择用 PowerShell 或 Terminal 打开。

   也可以手动进入：

   ```powershell
   cd D:\1\booking
   ```

3. 创建虚拟环境

   ```powershell
   py -3 -m venv .venv
   ```

4. 激活虚拟环境

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   如果 PowerShell 提示脚本执行被禁止，可以先运行：

   ```powershell
   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
   ```

   然后重新激活虚拟环境。

5. 安装依赖

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

6. 安装 Playwright Chromium 浏览器

   ```powershell
   python -m playwright install chromium
   ```

7. 创建 `.env`

   ```powershell
   copy .env.example .env
   ```

   然后用记事本打开 `.env`，把里面的占位符改成自己的信息：

   ```powershell
   notepad .env
   ```

8. 运行程序

   ```powershell
   python main.py
   ```

## macOS 从零开始运行

1. 安装 Python

   推荐从 Python 官网安装 Python 3.11 或更新版本：

   ```text
   https://www.python.org/downloads/macos/
   ```

2. 打开 Terminal，并进入项目文件夹

   如果项目在 Downloads 里，命令可能类似：

   ```bash
   cd ~/Downloads/booking
   ```

3. 创建虚拟环境

   ```bash
   python3 -m venv .venv
   ```

4. 激活虚拟环境

   ```bash
   source .venv/bin/activate
   ```

5. 安装依赖

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

6. 安装 Playwright Chromium 浏览器

   ```bash
   python -m playwright install chromium
   ```

7. 创建 `.env`

   ```bash
   cp .env.example .env
   ```

   然后用文本编辑器打开 `.env` 并填写账号信息。

8. 运行程序

   ```bash
   python main.py
   ```

## `.env` 配置方法

`.env` 用来保存账号信息。不要把 `.env` 发给别人，也不要提交到 Git。

最简单的单账号写法：

```dotenv
ACCOUNT_IDS=MAIN

MAIN_LABEL=My Account
MAIN_USERNAME=your_nottingham_username
MAIN_PASSWORD=your_password
MAIN_CONTACT_NO=your_phone_number
MAIN_FULL_NAME=Your Full Name
```

多账号写法：

```dotenv
ACCOUNT_IDS=MAIN,FRIEND

MAIN_LABEL=My Account
MAIN_USERNAME=your_nottingham_username
MAIN_PASSWORD=your_password
MAIN_CONTACT_NO=your_phone_number
MAIN_FULL_NAME=Your Full Name

FRIEND_LABEL=Friend Account
FRIEND_USERNAME=friends_nottingham_username
FRIEND_PASSWORD=friends_password
FRIEND_CONTACT_NO=friends_phone_number
FRIEND_FULL_NAME=Friend Full Name
```

说明：

- `ACCOUNT_IDS` 是账号列表，用英文逗号分隔。
- 如果 `ACCOUNT_IDS=MAIN,FRIEND`，下面就要写 `MAIN_...` 和 `FRIEND_...`。
- `USERNAME` 建议只填 Nottingham username，不要加 `@nottingham.edu.my`。
- `PASSWORD` 是登录密码。
- `CONTACT_NO` 会填进 booking form 的 contact number。
- `LABEL` 是 GUI 下拉框里显示的名称。
- `FULL_NAME` 当前主要作为配置保留项。

## 如何使用 GUI

运行 `python main.py` 后会先出现一个小窗口。

1. `Account`：选择要使用的账号。
2. `Facility`：选择 badminton court。
3. `Check-in`：用 date picker 选开始日期，用右侧下拉框选开始时间。
4. `Check-out`：用 date picker 选结束日期，用右侧下拉框选结束时间。
5. `Purpose`：填写用途，例如 `play badminton with friends`。
6. `Auto click Complete`：
   - 不勾选：程序会在最后点击 `Complete` 前暂停，适合手动检查。
   - 勾选：程序会自动点击 `Complete`，适合确认流程稳定后使用。
7. 点击 `Start Booking`。

当前默认日期是运行当天，默认时间是：

```text
Check-in: 18:01
Check-out: 20:00
```

## 常见问题

### 提示 `Missing ACCOUNT_IDS in .env`

说明没有创建 `.env`，或者 `.env` 不在项目根目录。

请确认项目根目录里有这个文件：

```text
.env
```

并且里面至少有：

```dotenv
ACCOUNT_IDS=MAIN
MAIN_USERNAME=your_nottingham_username
MAIN_PASSWORD=your_password
```

### 提示 `ModuleNotFoundError`

说明依赖没有装好，先确认虚拟环境已经激活，然后重新安装：

```powershell
pip install -r requirements.txt
```

macOS 用：

```bash
pip install -r requirements.txt
```

### 提示 Playwright 找不到浏览器

重新安装 Chromium：

```powershell
python -m playwright install chromium
```

macOS 同样使用：

```bash
python -m playwright install chromium
```

### 页面按钮找不到或脚本卡住

这个脚本依赖网页上的按钮名称和页面结构。如果学校网站更新了页面，脚本可能需要跟着更新 locator。

### 最后停在 `Complete` 前面

如果没有勾选 `Auto click Complete`，这是正常行为。请手动检查页面信息；如果确认无误，可以手动点击网页上的 `Complete`，或者下次运行时勾选 `Auto click Complete`。

## 可选：打包成 Windows `.exe`

当前最稳的方式仍然是直接运行 `python main.py`。如果要给不会 Python 的 Windows 用户使用，可以后续用 PyInstaller 打包。

这部分是给开发者使用的打包说明，不是普通用户的日常运行步骤。当前代码使用 `load_dotenv()` 自动查找 `.env`；如果打包后双击程序找不到 `.env`，需要后续把代码改成固定从程序所在文件夹读取 `.env`。

在 Windows 上运行：

```powershell
pip install pyinstaller
$env:PLAYWRIGHT_BROWSERS_PATH="0"
python -m playwright install chromium
python -m PyInstaller --noconfirm --onedir --windowed --name UNMBooking main.py
```

生成结果通常在：

```text
dist\UNMBooking\UNMBooking.exe
```

注意：

- 不建议把真实 `.env` 打包进 `.exe`。
- 可以把 `.env` 放在程序文件夹旁边，作为本地配置文件使用。
- Windows 的 `.exe` 只能给 Windows 用，不能给 macOS 用。

## 可选：打包成 macOS `.app`

macOS 需要在 Mac 上单独打包，不能直接使用 Windows 生成的 `.exe`。

这部分同样是给开发者使用的打包说明。当前代码使用 `load_dotenv()` 自动查找 `.env`；如果打包后双击程序找不到 `.env`，需要后续把代码改成固定从程序所在文件夹读取 `.env`。

在 macOS 上运行：

```bash
pip install pyinstaller
PLAYWRIGHT_BROWSERS_PATH=0 python -m playwright install chromium
python -m PyInstaller --noconfirm --onedir --windowed --name UNMBooking main.py
```

生成结果通常在：

```text
dist/UNMBooking.app
```

注意：

- 未签名的 `.app` 可能会被 macOS 安全机制拦截，需要手动允许打开。
- 如果要正式分发给很多人，后续应考虑 Apple Developer ID 签名和 notarization。
- macOS 的 `.app` 只能给 macOS 用，不能给 Windows 用。
