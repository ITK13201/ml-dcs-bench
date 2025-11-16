# ML-DCS-BENCH (Benchmark scripts of Machine Learning for Discrete Controller Synthesis)

[ML-DCS](https://github.com/ITK13201/ml-dcs/tree/master)のためのベンチマークスクリプト

## 目次

- [ML-DCS-BENCH (Benchmark scripts of Machine Learning for Discrete Controller Synthesis)](#ml-dcs-bench-benchmark-scripts-of-machine-learning-for-discrete-controller-synthesis)
  - [目次](#目次)
  - [概要](#概要)
  - [機能](#機能)
  - [必要要件](#必要要件)
  - [インストール](#インストール)
    - [ソースコードから](#ソースコードから)
    - [ビルド済みバイナリ](#ビルド済みバイナリ)
  - [使用方法](#使用方法)
    - [テストケースの作成](#テストケースの作成)
    - [ベンチマークの実行](#ベンチマークの実行)
    - [結果の統合](#結果の統合)
  - [プロジェクト構造](#プロジェクト構造)
  - [開発](#開発)
    - [開発環境のセットアップ](#開発環境のセットアップ)
    - [コードフォーマット](#コードフォーマット)
    - [実行ファイルのビルド](#実行ファイルのビルド)
  - [LTSコンポーネント](#ltsコンポーネント)
    - [評価シナリオ](#評価シナリオ)
      - [1. ArtGallery（Headcount Control）](#1-artgalleryheadcount-control)
      - [2. AT (Air Traffic)](#2-at-air-traffic)
      - [3. BW (Bidding Workflow)](#3-bw-bidding-workflow)
      - [4. CM (Cat and Mouse)](#4-cm-cat-and-mouse)
      - [5. KIVA\_system](#5-kiva_system)
    - [テストケース生成方法](#テストケース生成方法)
  - [結果フォーマット](#結果フォーマット)

## 概要

ML-DCS-BENCHは、MTSA（Modal Transition System Analyser）を使用した離散制御器合成アルゴリズムの評価を行うための包括的なベンチマークツールキットです。このツールキットは、LTS（Labeled Transition System）コンポーネントからのテストケース生成、合成ベンチマークの実行、パフォーマンスメトリクスの集約プロセスを自動化します。

## 機能

- **自動テストケース生成**: LTSコンポーネントの安全性プロパティのべき集合組み合わせからテストケースを生成
- **MTSA統合**: 設定可能なパラメータでMTSAを使用した制御器合成の実行
- **パフォーマンス監視**: 各ベンチマークの実行時間とメモリ使用量を追跡
- **結果集約**: 複数のベンチマーク結果を統合して包括的な分析を実施
- **クロスプラットフォーム対応**: Windows、macOS、Linux用のスタンドアロン実行ファイルをビルド

## 必要要件

- Python 3.12
- pipenv
- Java Runtime Environment（MTSA実行用）
- MTSAのjarファイル

## インストール

### ソースコードから

1. リポジトリをクローン:
```bash
git clone <repository-url>
cd ml-dcs-bench
```

2. プロジェクトディレクトリに移動:
```bash
cd ml-dcs-bench
```

3. 依存関係をインストール:
```bash
pip install pipenv
pipenv install
```

### ビルド済みバイナリ

[Releases](https://github.com/your-repo/releases)ページから、お使いのプラットフォーム用の最新リリースをダウンロードしてください。

## 使用方法

### テストケースの作成

LTSコンポーネントからテストケースを生成:

```bash
# Pythonを使用
pipenv run python main.py create_testcases -o ./tmp/testcases -O

# Makefileを使用
make create
```

**オプション:**
- `-l, --lts-components`: 処理するLTSコンポーネント名のリスト（デフォルト: 全コンポーネント）
- `-o, --output-dir`: 生成されたテストケースの出力ディレクトリ（デフォルト: `./tmp/testcases`）
- `-O, --overwrite`: 既存の出力ディレクトリを上書き

このコマンドは以下の手順でテストケースを生成します:
1. `assets/lts-components/<component-name>/`からLTSコンポーネントを読み込み
2. 安全性プロパティの組み合わせを作成（べき集合またはランダムサンプリング）
3. モデル、制御器仕様、ターゲットを組み合わせた`.lts`ファイルを出力

### ベンチマークの実行

テストケースに対してMTSAベンチマークを実行:

```bash
# Pythonを使用（デバッグモード）
make debug

# コンパイル済みバイナリを使用
make run
```

**オプション:**
- `-i, --input-dir`: テストケース`.lts`ファイルを含むディレクトリ（必須）
- `-o, --output-base-dir`: 出力ファイルのベースディレクトリ（必須）
- `-l, --log-base-dir`: ログファイルのベースディレクトリ（必須）
- `-s, --sleep-time`: タスク間のスリープ時間（秒）（デフォルト: 10）
- `-S, --skip-to`: 指定したテストケースまでスキップ（中断した実行の再開用）
- `-j, --mtsa-jar-path`: MTSAのjarファイルへのパス（必須）
- `-m, --memory-size`: Javaヒープメモリサイズ（GB）（デフォルト: 225）
- `-c, --mtsa-command`: 実行するMTSAコマンド（必須）
- `-t, --mtsa-target`: MTSAターゲット名（デフォルト: "TraditionalController"）
- `-M, --mtsa-result-mode`: MTSA結果モード（必須）

**実行例:**
```bash
pipenv run python main.py run \
  --input-dir ./tmp/testcases \
  --output-base-dir ./tmp/mtsa/output \
  --log-base-dir ./tmp/mtsa/log \
  --sleep-time 20 \
  --mtsa-jar-path ./tmp/mtsa/mtsa-PCS_MachineLearning_v0.2.3.jar \
  --memory-size 20 \
  --mtsa-command compose \
  --mtsa-target TraditionalController \
  --mtsa-result-mode for-machine-learning-extra
```

このコマンドの動作:
1. 各`.lts`ファイルをMTSAで処理
2. 実行中のメモリ使用量を監視
3. stdout/stderrを個別のログファイルに記録
4. タイミング、成功/失敗、メモリメトリクスを記録
5. タスク詳細を含む結果JSONファイルを出力

### 結果の統合

複数の結果ファイルをマージ:

```bash
# Pythonを使用
pipenv run python main.py combine_results \
  --results-dir ./tmp/mtsa/output \
  --output ./tmp/combined-result.json

# Makefileを使用
make combine
```

**オプション:**
- `-d, --results-dir`: 結果JSONファイルを含むディレクトリ
- `-f, --result-files`: 統合する特定の結果ファイル（複数回使用可能）
- `-o, --output`: 統合結果の出力ファイルパス（必須）

## プロジェクト構造

```
ml-dcs-bench/
├── ml-dcs-bench/
│   ├── main.py                 # アプリケーションエントリポイント
│   ├── ml_dcs_bench/
│   │   ├── cmd/               # コマンド実装
│   │   │   ├── root.py        # CLIルートコマンド
│   │   │   ├── create_testcases.py
│   │   │   ├── run.py
│   │   │   └── combine_results.py
│   │   ├── domain/            # ドメインモデル
│   │   │   ├── lts.py         # LTSと制御器仕様モデル
│   │   │   └── result.py      # ベンチマーク結果モデル
│   │   └── config/            # 設定とロギング
│   ├── assets/
│   │   └── lts-components/    # LTSコンポーネント定義
│   ├── Pipfile                # Python依存関係
│   ├── Makefile               # 共通タスク
│   └── pyproject.toml         # プロジェクトメタデータ
└── README.md
```

## 開発

### 開発環境のセットアップ

```bash
cd ml-dcs-bench
pipenv install --dev
pipenv shell
```

### コードフォーマット

Blackとisortでコードをフォーマット:

```bash
pipenv run black .
pipenv run isort .
```

設定は`pyproject.toml`で定義されています:
- 行の長さ: 88
- インポート並び替え: Black互換プロファイル

### 実行ファイルのビルド

プロジェクトはGitHub ActionsとNuitkaを使用してスタンドアロン実行ファイルをビルドします。ビルドをトリガーするには:

1. 新しいバージョンをタグ付け:
```bash
git tag v1.0.0
git push origin v1.0.0
```

2. GitHub Actionsが自動的にWindows、macOS、Linux用の実行ファイルをビルドしてリリースします。

## LTSコンポーネント

LTSコンポーネントは`ml-dcs-bench/assets/lts-components/<component-name>/`に格納されています。各コンポーネントディレクトリには以下が含まれます:

- `models.lts`: LTSモデル定義
- `cspec.yaml`: 制御器仕様（以下を含む）:
  - `name`: 制御器仕様名
  - `safety`: 安全性プロパティのリスト
  - `controllable`: 制御可能なアクションのリスト
  - `marking`: マーキングアクションのリスト（オプション）
  - `nonblocking`: ブール値フラグ（オプション）
- `targets.lts`: ターゲット仕様

### 評価シナリオ

DCSの入力である環境モデルと監視モデルを生成するため、以下の評価シナリオを使用します。各シナリオには環境モデルの数を変化させるパラメータ **N** と環境モデルあたりの状態数を変化させるパラメータ **K** があります。

#### 1. ArtGallery（Headcount Control）
部屋内の人数に応じて部屋への入室制御を行うシステム

- **パラメータ N**: 部屋の数
- **パラメータ K/S**: 部屋内の最大人数
- **バリアント**:
  - N variant: 2〜10部屋
  - S variant: 5〜10人

#### 2. AT (Air Traffic)
飛行機の着陸プロセスを指示することで複数の飛行機を衝突させずに着陸させるシステム

- **パラメータ N**: 飛行機の数（2〜5機）
- **パラメータ K**: 飛行機の着陸プロセスの数（2〜10プロセス）
- **構成例**: AT(2,2), AT(2,3), AT(3,4), AT(5,10)など

#### 3. BW (Bidding Workflow)
提出された申請書に対して審査チームで許可された申請書のみを受理するシステム

- **パラメータ N**: 審査チームの数（2〜5チーム）
- **パラメータ K**: 再申請可能回数（2〜5回）
- **構成例**: BW(2,2), BW(3,3), BW(5,5)など

#### 4. CM (Cat and Mouse)
捕獲ロボットを操作して制限されたエリア内で動く捕獲対象を捕獲するシステム

- **パラメータ N**: 捕獲対象の数（2〜5対象）
- **パラメータ K**: エリアの広さ（2〜5）
- **構成例**: CM(2,2), CM(3,4), CM(5,5)など

#### 5. KIVA_system
倉庫ロボットシステム（Amazon Roboticsベース）

- **パラメータ N**: ロボットの数
- **パラメータ S**: ポッドの数
- **バリアント**:
  - N variant: 2〜4ロボット
  - S variant: 5〜30ポッド

### テストケース生成方法

各シナリオには複数の監視モデル（安全性プロパティ）が存在します。テストケース生成では:

1. 監視モデルの組み合わせのべき集合を計算
2. べき集合が200個を超える場合は、最大200個の監視モデルの組をランダムに選択
3. 各組み合わせに対して環境モデルと組み合わせた`.lts`ファイルを生成

これにより、環境モデルと監視モデルの多様なペアを生成し、包括的なベンチマークテストを実現します。

## 結果フォーマット

ベンチマーク結果は以下の構造でJSON形式で保存されます:

```json
{
  "started_at": "ISO-8601タイムスタンプ",
  "finished_at": "ISO-8601タイムスタンプ",
  "task_count": 100,
  "task_success_count": 85,
  "task_failure_count": 15,
  "duration": "期間",
  "tasks": [
    {
      "name": "テストケース名",
      "success": true,
      "started_at": "ISO-8601タイムスタンプ",
      "finished_at": "ISO-8601タイムスタンプ",
      "max_memory_usage [KiB]": 1024000,
      "duration": "期間"
    }
  ]
}
```
