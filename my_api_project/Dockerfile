# ベースイメージを指定
FROM python:3.9

# 作業ディレクトリを指定
WORKDIR /app

# 依存パッケージのインストール
COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# アプリケーションのコードをコピー
COPY app /app

# デフォルトのコマンドを指定
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
