# 🎮 Roo-Tetris (ルーテトリス)

PythonとPygameで作成されたモダンなテトリスゲーム。このドキュメントも含めてすべてRooCode(with DeepSeek-r1)で生成しています。

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🚀 特徴
- モダンなゲームUI
- ハイスコアシステム
- ネクストテトリミノプレビュー
- 操作性の良い回転システム
- ゲームオーバー時のリスタート機能
- 効果音付き（WSL環境要設定）

## 🛠 動作環境
- Windows 10/11 + WSL2 (Ubuntu 22.04推奨)
- Python 3.10+
- PulseAudio (Windows側にインストール必要)

## 📥 インストール
```bash
git clone https://github.com/hama-jp/roo-tetris.git
cd roo-tetris
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 🎮 操作方法
| キー | 動作 |
|------|------|
| ←→   | 左右移動 |
| ↑    | 回転 |
| ↓    | 高速落下 |
| R    | リスタート |
| Q    | 終了 |

## 🎧 音声設定（WSL環境）
1. [Windows用PulseAudio](https://www.freedesktop.org/wiki/Software/PulseAudio/Ports/Windows/)をインストール
2. 管理者PowerShellで実行:
```powershell
SETX PULSE_SERVER tcp:localhost
pulseaudio.exe --start
```
3. WSLで再ログイン

## 📜 ライセンス
MIT License - [LICENSE](LICENSE)ファイルを参照

GitHub: [https://github.com/hama-jp/roo-tetris](https://github.com/hama-jp/roo-tetris)
