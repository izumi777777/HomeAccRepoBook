# Dockerfile

# ベースイメージ
FROM python:3.10

# 作業ディレクトリの設定
WORKDIR /app

# アプリケーションのソースコードをコピー
COPY . /app

# 必要なパッケージのインストール
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# ポートの公開
EXPOSE 5000

# アプリケーションの起動
CMD ["flask", "run", "--host=0.0.0.0"]
