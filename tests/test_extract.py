import os, shutil

from werkzeug.datastructures import FileStorage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from app import create_app
from app.utils import format_size


# ========== BLACK BOX ==========
class TestExtracting:
    def setup_method(self):
        """
        Thiết lập môi trường kiểm thử cho mỗi phương thức kiểm thử.

        - Tạo ứng dụng Flask.
        - Tạo và đẩy ngữ cảnh ứng dụng để có thể sử dụng các thành phần của ứng dụng trong kiểm thử.
        - Tạo client kiểm thử để gửi yêu cầu HTTP và nhận phản hồi.

        :return: None
        """
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)

    def teardown_method(self):
        """
        Dọn dẹp môi trường kiểm thử sau khi mỗi phương thức kiểm thử kết thúc.

        - Pop ngữ cảnh ứng dụng để giải phóng tài nguyên và đảm bảo sự sạch sẽ của môi trường.
        - Xóa các tệp tải lên trong thư mục 'uploads' để tránh ảnh hưởng đến các phương thức kiểm thử khác.

        :return: None
        """
        self.app_context.pop()
        folder = "uploads"
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print("Failed to delete %s. Reason: %s" % (file_path, e))

    def test_extract_page(self):
        """
        Kiểm thử trang "extract" để đảm bảo rằng nó chứa chuỗi "Extract file".

        - Gửi yêu cầu GET đến đường dẫn "/extract".
        - Kiểm tra xem phản hồi có chứa chuỗi "Extract file" hay không.

        :return: None
        """
        response = self.client.get("/extract")
        assert "Extract file" in response.get_data(as_text=True)

    def test_extract_success(self):
        """
        Kiểm thử quy trình nhúng và rút trích dữ liệu thành công.

        - Chuẩn bị dữ liệu cho việc nhúng và rút trích.
        - Gửi yêu cầu POST để nhúng dữ liệu vào tệp âm thanh.
        - Tạo đối tượng FileStorage cho tệp đã nhúng.
        - Gửi yêu cầu POST để rút trích dữ liệu.
        - Kiểm tra các điều kiện sau quy trình rút trích.

        :return: None
        """
        carrier_name = "wav-small.wav"
        data_name = "png.png"
        password = "abc"
        carrier_path = f"file_tests/{carrier_name}"
        data_path = f"file_tests/{data_name}"
        embedded_path = f"uploads/{carrier_name}"
        carrier_file = FileStorage(
            stream=open(carrier_path, "rb"),
            filename=carrier_name,
            content_type="audio/wav",
        )
        data_file = FileStorage(
            stream=open(data_path, "rb"),
            filename=data_name,
            content_type="image/png",
        )
        self.client.post(
            "/embed",
            data={
                "carrier": carrier_file,
                "data": data_file,
                "password": password,
                "confirm-password": password,
            },
            follow_redirects=True,
            content_type="multipart/form-data",
        )
        embedded_file = FileStorage(
            stream=open(embedded_path, "rb"),
            filename=carrier_name,
            content_type="audio/wav",
        )

        response = self.client.post(
            "/extract",
            data={
                "carrier": embedded_file,
                "password": password,
            },
            follow_redirects=True,
            content_type="multipart/form-data",
        )

        assert "Carrier file must be file wav." not in response.get_data(as_text=True)
        assert (
            "Carrier file size is too small for extractding."
            not in response.get_data(as_text=True)
        )
        assert "Passwords must match." not in response.get_data(as_text=True)
        assert "Download" in response.get_data(as_text=True)
        assert "Extracted File Information" in response.get_data(as_text=True)
        assert data_name in response.get_data(as_text=True)
        assert format_size(os.path.getsize(data_path)) in response.get_data(
            as_text=True
        )

    def test_extract_failed_due_to_passwords_not_match(self):
        """
        Kiểm thử trường hợp rút trích thất bại do mật khẩu không khớp.

        - Chuẩn bị dữ liệu cho việc nhúng và rút trích.
        - Gửi yêu cầu POST để nhúng dữ liệu vào tệp âm thanh.
        - Tạo đối tượng FileStorage cho tệp đã nhúng.
        - Gửi yêu cầu POST để rút trích dữ liệu với mật khẩu không khớp.
        - Kiểm tra các điều kiện sau quy trình rút trích thất bại.

        :return: None
        """
        carrier_name = "wav-small.wav"
        data_name = "png.png"
        password = "abc"
        carrier_path = f"file_tests/{carrier_name}"
        data_path = f"file_tests/{data_name}"
        embedded_path = f"uploads/{carrier_name}"
        carrier_file = FileStorage(
            stream=open(carrier_path, "rb"),
            filename=carrier_name,
            content_type="audio/wav",
        )
        data_file = FileStorage(
            stream=open(data_path, "rb"),
            filename=data_name,
            content_type="image/png",
        )
        self.client.post(
            "/embed",
            data={
                "carrier": carrier_file,
                "data": data_file,
                "password": password,
                "confirm-password": password,
            },
            follow_redirects=True,
            content_type="multipart/form-data",
        )
        embedded_file = FileStorage(
            stream=open(embedded_path, "rb"),
            filename=carrier_name,
            content_type="audio/wav",
        )

        response = self.client.post(
            "/extract",
            data={
                "carrier": embedded_file,
                "password": password + "123",
            },
            follow_redirects=True,
            content_type="multipart/form-data",
        )

        assert "Carrier file must be file wav." not in response.get_data(as_text=True)
        assert (
            "Carrier file size is too small for extractding."
            not in response.get_data(as_text=True)
        )
        assert "Password must match." in response.get_data(as_text=True)
        assert "Download" not in response.get_data(as_text=True)
        assert "Extracted File Information" not in response.get_data(as_text=True)
        assert data_name not in response.get_data(as_text=True)
        assert format_size(os.path.getsize(data_path)) not in response.get_data(
            as_text=True
        )

    def test_extract_failed_due_to_not_embedded_file(self):
        """
        Kiểm thử trường hợp rút trích thất bại do không có tệp đã nhúng.

        - Chuẩn bị dữ liệu cho việc rút trích.
        - Gửi yêu cầu POST để rút trích dữ liệu từ tệp không có sự nhúng.
        - Kiểm tra các điều kiện sau quy trình rút trích thất bại.

        :return: None
        """
        carrier_name = "wav-small.wav"
        data_name = "png.png"
        password = "abc"
        data_path = f"file_tests/{data_name}"
        embedded_path = f"file_tests/{carrier_name}"
        embedded_file = FileStorage(
            stream=open(embedded_path, "rb"),
            filename=carrier_name,
            content_type="audio/wav",
        )

        response = self.client.post(
            "/extract",
            data={
                "carrier": embedded_file,
                "password": password,
            },
            follow_redirects=True,
            content_type="multipart/form-data",
        )

        assert "Embedded file must be file wav." not in response.get_data(as_text=True)
        assert "This is not an embedded file." in response.get_data(as_text=True)
        assert "Password must match." not in response.get_data(as_text=True)
        assert "Download" not in response.get_data(as_text=True)
        assert "Extracted File Information" not in response.get_data(as_text=True)
        assert data_name not in response.get_data(as_text=True)
        assert format_size(os.path.getsize(data_path)) not in response.get_data(
            as_text=True
        )

    def test_extract_failed_due_to_invalid_carrier_file_format(self):
        """
        Kiểm thử trường hợp rút trích thất bại do định dạng không hợp lệ của tệp âm thanh.

        - Chuẩn bị dữ liệu cho việc rút trích.
        - Gửi yêu cầu POST để rút trích dữ liệu từ tệp âm thanh có định dạng không hợp lệ.
        - Kiểm tra các điều kiện sau quy trình rút trích thất bại.

        :return: None
        """
        carrier_name = "mp3.mp3"
        data_name = "png.png"
        password = "abc"
        data_path = f"file_tests/{data_name}"
        embedded_path = f"file_tests/{carrier_name}"
        embedded_file = FileStorage(
            stream=open(embedded_path, "rb"),
            filename=carrier_name,
            content_type="audio/wav",
        )

        response = self.client.post(
            "/extract",
            data={
                "carrier": embedded_file,
                "password": password,
            },
            follow_redirects=True,
            content_type="multipart/form-data",
        )

        assert "Embedded file must be file wav." in response.get_data(as_text=True)
        assert (
            "Carrier file size is too small for extractding."
            not in response.get_data(as_text=True)
        )
        assert "Password must match." not in response.get_data(as_text=True)
        assert "Download" not in response.get_data(as_text=True)
        assert "Extracted File Information" not in response.get_data(as_text=True)
        assert data_name not in response.get_data(as_text=True)
        assert format_size(os.path.getsize(data_path)) not in response.get_data(
            as_text=True
        )


class TestExtractdingSelenium:
    def setup_method(self):
        """
        Thiết lập môi trường cho việc kiểm thử Selenium.

        - Tạo ứng dụng Flask.
        - Kích hoạt bối cảnh ứng dụng.
        - Khởi tạo đối tượng test client.
        - Cấu hình trình duyệt Chrome để chạy ở chế độ "headless".
        - Khởi tạo đối tượng trình duyệt Chrome với các tùy chọn đã cấu hình.
        - Thiết lập đường dẫn kiểm thử cho trang rút trích.

        :return: None
        """
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)

        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.browser = webdriver.Chrome(options=self.chrome_options)
        self.testing_path = "http://localhost:3000/extract"

    def teardown_method(self):
        """
        Dọn dẹp sau khi kết thúc kiểm thử.

        - Đẩy bối cảnh ứng dụng khỏi ngăn xếp để giải phóng tài nguyên.
        - Xóa tất cả các tệp trong thư mục "uploads".

        :return: None
        """
        self.app_context.pop()
        folder = "uploads"
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print("Failed to delete %s. Reason: %s" % (file_path, e))

    def __get_abs_path(self, path1, path2):
        return os.path.join("D:/Workspace/audio_steganography", path1, path2)

    def test_extract_page(self):
        """
        Kiểm thử hiển thị trang rút trích.

        - Truy cập trang rút trích bằng trình duyệt tự động.
        - Kiểm tra tiêu đề của trang và tiêu đề chính xác.

        :return: None
        """
        self.browser.get(f"{self.testing_path}")

        title_element = self.browser.find_element(By.TAG_NAME, "h3")

        assert "Audio Steganography" in self.browser.title
        assert title_element.text == "Extract file"

    def test_extract_success(self):
        """
        Kiểm thử quá trình rút trích thành công.

        - Chuẩn bị dữ liệu cho quá trình rút trích.
        - Gửi yêu cầu POST để nhúng dữ liệu vào tệp âm thanh.
        - Mở trình duyệt tự động và điền thông tin cần thiết.
        - Thực hiện quá trình rút trích thông qua giao diện người dùng trình duyệt.
        - Kiểm tra kết quả rút trích thành công.

        :return: None
        """
        carrier_name = "wav-small.wav"
        data_name = "png.png"
        password = "abc"
        carrier_path = f"file_tests/{carrier_name}"
        data_path = f"file_tests/{data_name}"
        carrier_file = FileStorage(
            stream=open(carrier_path, "rb"),
            filename=carrier_name,
            content_type="audio/wav",
        )
        data_file = FileStorage(
            stream=open(data_path, "rb"),
            filename=data_name,
            content_type="image/png",
        )
        self.client.post(
            "/embed",
            data={
                "carrier": carrier_file,
                "data": data_file,
                "password": password,
                "confirm-password": password,
            },
            follow_redirects=True,
            content_type="multipart/form-data",
        )
        self.browser.get(self.testing_path)
        embedded_file_input = self.browser.find_element(By.ID, "carrier")
        password_input = self.browser.find_element(By.ID, "password")
        extract_button = self.browser.find_element(
            By.CSS_SELECTOR, "button[type='submit']"
        )

        embedded_file_input.send_keys(self.__get_abs_path("uploads", carrier_name))
        password_input.send_keys(password)
        self.browser.execute_script("arguments[0].click();", extract_button)
        html = self.browser.page_source

        assert "Carrier file must be file wav." not in html
        assert "Carrier file size is too small for extractding." not in html
        assert "Passwords must match." not in html
        assert "Download" in html
        assert "Extracted File Information" in html
        assert data_name in html
        assert (
            format_size(os.path.getsize(self.__get_abs_path("file_tests", data_name)))
            in html
        )

    def test_extract_failed_due_to_passwords_not_match(self):
        """
        Kiểm thử trường hợp rút trích thất bại do mật khẩu không khớp.

        - Chuẩn bị dữ liệu cho quá trình rút trích.
        - Gửi yêu cầu POST để nhúng dữ liệu vào tệp âm thanh.
        - Mở trình duyệt tự động và điền thông tin cần thiết.
        - Thực hiện quá trình rút trích thông qua giao diện người dùng trình duyệt với mật khẩu không khớp.
        - Kiểm tra kết quả rút trích thất bại.

        :return: None
        """
        carrier_name = "wav-small.wav"
        data_name = "png.png"
        password = "abc"
        carrier_path = f"file_tests/{carrier_name}"
        data_path = f"file_tests/{data_name}"
        carrier_file = FileStorage(
            stream=open(carrier_path, "rb"),
            filename=carrier_name,
            content_type="audio/wav",
        )
        data_file = FileStorage(
            stream=open(data_path, "rb"),
            filename=data_name,
            content_type="image/png",
        )
        self.client.post(
            "/embed",
            data={
                "carrier": carrier_file,
                "data": data_file,
                "password": password,
                "confirm-password": password,
            },
            follow_redirects=True,
            content_type="multipart/form-data",
        )
        self.browser.get(self.testing_path)
        embedded_file_input = self.browser.find_element(By.ID, "carrier")
        password_input = self.browser.find_element(By.ID, "password")
        extract_button = self.browser.find_element(
            By.CSS_SELECTOR, "button[type='submit']"
        )

        embedded_file_input.send_keys(self.__get_abs_path("uploads", carrier_name))
        password_input.send_keys(password + "123")
        self.browser.execute_script("arguments[0].click();", extract_button)
        html = self.browser.page_source

        assert "Carrier file must be file wav." not in html
        assert "Carrier file size is too small for extractding." not in html
        assert "Password must match." in html
        assert "Download" not in html
        assert "Extracted File Information" not in html
        assert data_name not in html
        assert (
            format_size(os.path.getsize(self.__get_abs_path("file_tests", data_name)))
            not in html
        )

    def test_extract_failed_due_to_not_embedded_file(self):
        """
        Kiểm thử trường hợp rút trích thất bại do tệp âm thanh không chứa dữ liệu nhúng.

        - Chuẩn bị dữ liệu cho quá trình rút trích.
        - Gửi yêu cầu POST để rút trích từ tệp âm thanh không chứa dữ liệu.
        - Kiểm tra kết quả rút trích thất bại.

        :return: None
        """
        carrier_name = "wav-small.wav"
        data_name = "png.png"
        password = "abc"
        data_path = f"file_tests/{data_name}"
        embedded_path = f"file_tests/{carrier_name}"
        embedded_file = FileStorage(
            stream=open(embedded_path, "rb"),
            filename=carrier_name,
            content_type="audio/wav",
        )

        response = self.client.post(
            "/extract",
            data={
                "carrier": embedded_file,
                "password": password,
            },
            follow_redirects=True,
            content_type="multipart/form-data",
        )

        assert "Embedded file must be file wav." not in response.get_data(as_text=True)
        assert "This is not an embedded file." in response.get_data(as_text=True)
        assert "Password must match." not in response.get_data(as_text=True)
        assert "Download" not in response.get_data(as_text=True)
        assert "Extracted File Information" not in response.get_data(as_text=True)
        assert data_name not in response.get_data(as_text=True)
        assert format_size(os.path.getsize(data_path)) not in response.get_data(
            as_text=True
        )

    def test_extract_failed_due_to_invalid_carrier_file_format(self):
        """
        Kiểm thử trường hợp rút trích thất bại do định dạng tệp âm thanh không hợp lệ.

        - Chuẩn bị dữ liệu cho quá trình rút trích.
        - Sử dụng Selenium để điều hướng trình duyệt và gửi yêu cầu POST.
        - Kiểm tra kết quả rút trích thất bại.

        :return: None
        """
        carrier_name = "mp3.mp3"
        data_name = "png.png"
        password = "abc"
        self.browser.get(self.testing_path)
        embedded_file_input = self.browser.find_element(By.ID, "carrier")
        password_input = self.browser.find_element(By.ID, "password")
        extract_button = self.browser.find_element(
            By.CSS_SELECTOR, "button[type='submit']"
        )

        embedded_file_input.send_keys(self.__get_abs_path("file_tests", carrier_name))
        password_input.send_keys(password)
        self.browser.execute_script("arguments[0].click();", extract_button)
        html = self.browser.page_source

        assert "Embedded file must be file wav." in html
        assert "Carrier file size is too small for extractding." not in html
        assert "Password must match." not in html
        assert "Download" not in html
        assert "Extracted File Information" not in html
        assert data_name not in html
        assert (
            format_size(os.path.getsize(self.__get_abs_path("file_tests", data_name)))
            not in html
        )
