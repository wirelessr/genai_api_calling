# 使用官方的Python基礎映像檔
FROM python:3.9

# 設定工作目錄
WORKDIR /app

# 複製當前目錄到工作目錄
COPY . .

# 安裝需要的Python套件
RUN pip install --no-cache-dir -r requirements.txt

# 暴露應用程式的埠號
EXPOSE 5000

# 執行Flask應用程式
CMD ["python", "app.py"]

