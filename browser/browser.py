from playwright.sync_api import sync_playwright


class Browser:

    def open(self):

        playwright = sync_playwright().start()

        context = playwright.chromium.launch_persistent_context(
            user_data_dir=r"C:\ChromePriceMonitor",
            executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            channel="chrome",
            headless=False,
            viewport={"width": 1400, "height": 900},
            locale="pt-BR",
        )

        page = context.new_page()

        return playwright, context, page