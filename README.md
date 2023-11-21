# Audio Steganography

Ứng dụng giúp che giấu file trong file audio (.wav, ...)

## Hướng dẫn Chạy Dự Án Flask

1. **Clone Repository:**
   ```bash
   git clone https://github.com/tranlequocthong313/audio_steganography.git
   ```

2. **Di chuyển vào thư mục Dự án:**
   ```bash
   cd audio_steganography
   ```

3. **Tạo Môi Trường Ảo (Optional, nhưng được khuyến khích):**
   ```bash
   python -m venv venv
   ```

4. **Truy Cập vào Môi Trường Ảo:**
   - **Windows:**
     ```bash
     .\venv\Scripts\activate
     ```

   - **Bash:**
     ```bash
     source venv/bin/activate
     ```

5. **Cài đặt thư viện:**
   ```bash
   pip install -r requirements.txt
   ```

6. **Chạy ứng dụng:**
   - **Windows:**
   ```bash
   set FLASK_APP=app && flask run --debug
   ```

   - **Bash:**
   ```bash
   export FLASK_APP='app' && flask run --debug
   ```
