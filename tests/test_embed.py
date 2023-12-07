import os, shutil

from werkzeug.datastructures import FileStorage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from app import create_app
from app.utils import format_size


# ========== BLACK BOX ==========
class TestEmbedding:
    def setup_method(self):
        """
        Thiết lập môi trường cho mỗi phương thức kiểm thử.

        - Tạo ứng dụng Flask.
        - Kích hoạt ngữ cảnh ứng dụng.
        - Tạo đối tượng client để thực hiện các yêu cầu HTTP trong quá trình kiểm thử.

        :return: None
        """
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)

    def teardown_method(self):
        """
        Dọn dẹp sau mỗi phương thức kiểm thử.

        - Hủy kích hoạt ngữ cảnh ứng dụng.
        - Xóa các tệp tạm thời và thư mục tạo ra trong quá trình kiểm thử.

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

    def test_home_page(self):
        """
        Kiểm tra trang chủ của ứng dụng.

        - Gửi yêu cầu GET đến trang chủ.
        - Kiểm tra xem trang chủ có chứa chuỗi "Embed file" hay không.

        :return: None
        """
        response = self.client.get("/")
        assert "Embed file" in response.get_data(as_text=True)

    def test_embed_page(self):
        """
        Kiểm tra trang nhúng file của ứng dụng.

        - Gửi yêu cầu GET đến trang nhúng file.
        - Kiểm tra xem trang nhúng file có chứa chuỗi "Embed file" hay không.

        :return: None
        """
        response = self.client.get("/embed")
        assert "Embed file" in response.get_data(as_text=True)

    def test_embed_success(self):
        """
        Kiểm tra quá trình nhúng file thành công.

        - Chuẩn bị tên file carrier, tên file data, mật khẩu và đường dẫn tới file carrier và data.
        - Tạo đối tượng FileStorage cho carrier và data.
        - Gửi yêu cầu POST đến trang nhúng file với các tham số cần thiết.
        - Kiểm tra kết quả trả về để đảm bảo rằng:
            + Không có thông báo lỗi về định dạng carrier.
            + Carrier có kích thước đủ lớn cho việc nhúng.
            + Mật khẩu trùng khớp.
            + Trang hiển thị nút Download và thông tin về file đã nhúng.

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

        response = self.client.post(
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

        assert "Carrier file must be file wav." not in response.get_data(as_text=True)
        assert "Carrier file size is too small for embedding." not in response.get_data(
            as_text=True
        )
        assert "Passwords must match." not in response.get_data(as_text=True)
        assert "Download" in response.get_data(as_text=True)
        assert "Embedded File Information" in response.get_data(as_text=True)
        assert carrier_name in response.get_data(as_text=True)
        assert format_size(os.path.getsize(carrier_path)) in response.get_data(
            as_text=True
        )

    def test_embed_failed_due_to_passwords_not_match(self):
        """
        Kiểm tra quá trình nhúng file thất bại do mật khẩu không trùng khớp.

        - Chuẩn bị tên file carrier, tên file data, mật khẩu và đường dẫn tới file carrier và data.
        - Tạo đối tượng FileStorage cho carrier và data.
        - Gửi yêu cầu POST đến trang nhúng file với các tham số cần thiết, nhưng mật khẩu không khớp.
        - Kiểm tra kết quả trả về để đảm bảo rằng:
            + Không có thông báo lỗi về định dạng carrier.
            + Carrier có kích thước đủ lớn cho việc nhúng.
            + Mật khẩu không trùng khớp.
            + Trang không hiển thị nút Download và thông tin về file đã nhúng.

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

        response = self.client.post(
            "/embed",
            data={
                "carrier": carrier_file,
                "data": data_file,
                "password": password,
                "confirm-password": password + "123",
            },
            follow_redirects=True,
            content_type="multipart/form-data",
        )

        assert "Carrier file must be file wav." not in response.get_data(as_text=True)
        assert "Carrier file size is too small for embedding." not in response.get_data(
            as_text=True
        )
        assert "Passwords must match." in response.get_data(as_text=True)
        assert "Download" not in response.get_data(as_text=True)
        assert "Embedded File Information" not in response.get_data(as_text=True)
        assert carrier_name not in response.get_data(as_text=True)
        assert format_size(os.path.getsize(carrier_path)) not in response.get_data(
            as_text=True
        )

    def test_embed_failed_due_to_size_overflowed(self):
        """
        Kiểm tra quá trình nhúng file thất bại do kích thước file vượt quá dung lượng cho phép.

        - Chuẩn bị tên file carrier, tên file data, mật khẩu và đường dẫn tới file carrier và data.
        - Tạo đối tượng FileStorage cho carrier và data.
        - Gửi yêu cầu POST đến trang nhúng file với các tham số cần thiết.
        - Kiểm tra kết quả trả về để đảm bảo rằng:
            + Không có thông báo lỗi về định dạng carrier.
            + Kích thước của carrier nhỏ hơn dung lượng cho phép.
            + Mật khẩu không trùng khớp.
            + Trang không hiển thị nút Download và thông tin về file đã nhúng.

        :return: None
        """
        carrier_name = "wav-small.wav"
        data_name = "mp3.mp3"
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

        response = self.client.post(
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

        assert "Carrier file must be file wav." not in response.get_data(as_text=True)
        assert "Carrier file size is too small for embedding." in response.get_data(
            as_text=True
        )
        assert "Passwords must match." not in response.get_data(as_text=True)
        assert "Download" not in response.get_data(as_text=True)
        assert "Embedded File Information" not in response.get_data(as_text=True)
        assert carrier_name not in response.get_data(as_text=True)
        assert format_size(os.path.getsize(carrier_path)) not in response.get_data(
            as_text=True
        )

    def test_embed_failed_due_to_invalid_carrier_file_format(self):
        """
        Kiểm tra quá trình nhúng file thất bại do định dạng không hợp lệ của carrier.

        - Chuẩn bị tên file carrier, tên file data, mật khẩu và đường dẫn tới file carrier và data.
        - Tạo đối tượng FileStorage cho carrier và data.
        - Gửi yêu cầu POST đến trang nhúng file với các tham số cần thiết.
        - Kiểm tra kết quả trả về để đảm bảo rằng:
            + Hiển thị thông báo lỗi về định dạng carrier.
            + Kích thước của carrier nhỏ hơn dung lượng cho phép.
            + Mật khẩu không trùng khớp.
            + Trang không hiển thị nút Download và thông tin về file đã nhúng.

        :return: None
        """
        carrier_name = "mp3.mp3"
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

        response = self.client.post(
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

        assert "Carrier file must be file wav." in response.get_data(as_text=True)
        assert "Carrier file size is too small for embedding." not in response.get_data(
            as_text=True
        )
        assert "Passwords must match." not in response.get_data(as_text=True)
        assert "Download" not in response.get_data(as_text=True)
        assert "Embedded File Information" not in response.get_data(as_text=True)
        assert carrier_name not in response.get_data(as_text=True)
        assert format_size(os.path.getsize(carrier_path)) not in response.get_data(
            as_text=True
        )


class TestEmbeddingSelenium:
    def setup_method(self):
        """
        Thiết lập môi trường cho việc kiểm thử Selenium.

        - Tạo ứng dụng Flask.
        - Tạo cấu hình cho trình duyệt Chrome để chạy ở chế độ headless.
        - Khởi tạo trình duyệt Chrome với các tùy chọn đã cấu hình.
        - Thiết lập đường dẫn thử nghiệm cho việc kiểm thử Selenium.

        :return: None
        """
        self.app = create_app()
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.browser = webdriver.Chrome(options=self.chrome_options)
        self.testing_path = "http://localhost:3000"

    def teardown_method(self):
        """
        Dọn dẹp tài nguyên sau mỗi phương thức kiểm thử.

        - Duyệt qua tất cả các tệp trong thư mục "uploads".
        - Xóa tất cả các tệp và thư mục trong "uploads".

        :return: None
        """
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

    def __get_abs_path(self, path):
        return os.path.join("D:/Workspace/audio_steganography", "file_tests", path)

    def test_home_page(self):
        """
        Kiểm tra trang chủ của ứng dụng web.

        - Mở trình duyệt và truy cập trang chủ.
        - Kiểm tra tiêu đề trình duyệt và tiêu đề trang có phù hợp không.

        :return: None
        """
        self.browser.get(self.testing_path)

        title_element = self.browser.find_element(By.TAG_NAME, "h3")

        assert "Audio Steganography" in self.browser.title
        assert title_element.text == "Embed file"

    def test_embed_page(self):
        """
        Kiểm tra trang nhúng tệp của ứng dụng web.

        - Mở trình duyệt và truy cập trang nhúng.
        - Kiểm tra tiêu đề trình duyệt và tiêu đề trang có phù hợp không.

        :return: None
        """
        self.browser.get(f"{self.testing_path}/embed")

        title_element = self.browser.find_element(By.TAG_NAME, "h3")

        assert "Audio Steganography" in self.browser.title
        assert title_element.text == "Embed file"

    def test_embed_success(self):
        """
        Kiểm tra quá trình nhúng tệp thành công.

        - Mở trình duyệt và truy cập trang nhúng.
        - Điền thông tin cần thiết: tệp carrier, tệp data, mật khẩu, xác nhận mật khẩu.
        - Nhấn nút nhúng và kiểm tra kết quả trên trang.

        :return: None
        """
        carrier_name = "wav-small.wav"
        data_name = "png.png"
        password = "abc"
        self.browser.get(self.testing_path)
        carrier_file_input = self.browser.find_element(By.ID, "carrier")
        data_file_input = self.browser.find_element(By.ID, "data")
        password_input = self.browser.find_element(By.ID, "password")
        confirm_password_input = self.browser.find_element(By.ID, "confirm-password")
        embed_button = self.browser.find_element(
            By.CSS_SELECTOR, "button[type='submit']"
        )

        carrier_file_input.send_keys(self.__get_abs_path(carrier_name))
        data_file_input.send_keys(self.__get_abs_path(data_name))
        password_input.send_keys(password)
        confirm_password_input.send_keys(password)
        self.browser.execute_script("arguments[0].click();", embed_button)
        html = self.browser.page_source

        assert "Carrier file must be file wav." not in html
        assert "Carrier file size is too small for embedding." not in html
        assert "Passwords must match." not in html
        assert "Download" in html
        assert "Embedded File Information" in html
        assert carrier_name in html
        assert format_size(os.path.getsize(self.__get_abs_path(carrier_name))) in html

    def test_embed_failed_due_to_passwords_not_match(self):
        """
        Kiểm tra quá trình nhúng tệp thất bại do mật khẩu không khớp.

        - Mở trình duyệt và truy cập trang nhúng.
        - Điền thông tin cần thiết: tệp carrier, tệp data, mật khẩu, xác nhận mật khẩu không khớp.
        - Nhấn nút nhúng và kiểm tra kết quả trên trang.

        :return: None
        """
        carrier_name = "wav-small.wav"
        data_name = "png.png"
        password = "abc"
        self.browser.get(self.testing_path)
        carrier_file_input = self.browser.find_element(By.ID, "carrier")
        data_file_input = self.browser.find_element(By.ID, "data")
        password_input = self.browser.find_element(By.ID, "password")
        confirm_password_input = self.browser.find_element(By.ID, "confirm-password")
        embed_button = self.browser.find_element(
            By.CSS_SELECTOR, "button[type='submit']"
        )

        carrier_file_input.send_keys(self.__get_abs_path(carrier_name))
        data_file_input.send_keys(self.__get_abs_path(data_name))
        password_input.send_keys(password)
        confirm_password_input.send_keys(password + "123")
        self.browser.execute_script("arguments[0].click();", embed_button)
        html = self.browser.page_source

        assert "Carrier file must be file wav." not in html
        assert "Carrier file size is too small for embedding." not in html
        assert "Passwords must match." in html
        assert "Download" not in html
        assert "Embedded File Information" not in html
        assert carrier_name not in html
        assert (
            format_size(os.path.getsize(self.__get_abs_path(carrier_name))) not in html
        )

    def test_embed_failed_due_to_size_overflowed(self):
        """
        Kiểm tra quá trình nhúng tệp thất bại do kích thước tệp vượt quá giới hạn.

        - Mở trình duyệt và truy cập trang nhúng.
        - Điền thông tin cần thiết: tệp carrier, tệp data với kích thước lớn hơn giới hạn cho phép, mật khẩu, và xác nhận mật khẩu.
        - Nhấn nút nhúng và kiểm tra kết quả trên trang.

        :return: None
        """
        carrier_name = "wav-small.wav"
        data_name = "mp3.mp3"
        password = "abc"
        self.browser.get(self.testing_path)
        carrier_file_input = self.browser.find_element(By.ID, "carrier")
        data_file_input = self.browser.find_element(By.ID, "data")
        password_input = self.browser.find_element(By.ID, "password")
        confirm_password_input = self.browser.find_element(By.ID, "confirm-password")
        embed_button = self.browser.find_element(
            By.CSS_SELECTOR, "button[type='submit']"
        )

        carrier_file_input.send_keys(self.__get_abs_path(carrier_name))
        data_file_input.send_keys(self.__get_abs_path(data_name))
        password_input.send_keys(password)
        confirm_password_input.send_keys(password)
        self.browser.execute_script("arguments[0].click();", embed_button)
        html = self.browser.page_source

        assert "Carrier file must be file wav." not in html
        assert "Carrier file size is too small for embedding." in html
        assert "Passwords must match." not in html
        assert "Download" not in html
        assert "Embedded File Information" not in html
        assert carrier_name not in html
        assert (
            format_size(os.path.getsize(self.__get_abs_path(carrier_name))) not in html
        )

    def test_embed_failed_due_to_invalid_carrier_file_format(self):
        """
        Kiểm tra quá trình nhúng tệp thất bại do định dạng tệp carrier không hợp lệ.

        - Mở trình duyệt và truy cập trang nhúng.
        - Điền thông tin cần thiết: tệp carrier với định dạng không hợp lệ, tệp data, mật khẩu, và xác nhận mật khẩu.
        - Nhấn nút nhúng và kiểm tra kết quả trên trang.

        :return: None
        """
        carrier_name = "mp3.mp3"
        data_name = "png.png"
        password = "abc"
        self.browser.get(self.testing_path)
        carrier_file_input = self.browser.find_element(By.ID, "carrier")
        data_file_input = self.browser.find_element(By.ID, "data")
        password_input = self.browser.find_element(By.ID, "password")
        confirm_password_input = self.browser.find_element(By.ID, "confirm-password")
        embed_button = self.browser.find_element(
            By.CSS_SELECTOR, "button[type='submit']"
        )

        carrier_file_input.send_keys(self.__get_abs_path(carrier_name))
        data_file_input.send_keys(self.__get_abs_path(data_name))
        password_input.send_keys(password)
        confirm_password_input.send_keys(password)
        self.browser.execute_script("arguments[0].click();", embed_button)
        html = self.browser.page_source

        assert "Carrier file must be file wav." in html
        assert "Carrier file size is too small for embedding." not in html
        assert "Passwords must match." not in html
        assert "Download" not in html
        assert "Embedded File Information" not in html
        assert carrier_name not in html
        assert (
            format_size(os.path.getsize(self.__get_abs_path(carrier_name))) not in html
        )
