from playwright.async_api import async_playwright, expect

from app.models.library_book import get_books_due, LibraryBook
from app.utlis.logger import logger



class AutoRenewer:
    def __init__(self, config: dict) -> None:
        try:
            self.page = None
            self.config = config
            # set up emailer
            # self.emailer = Emailer()
        except Exception as e:
            error_msg = f'Failed to create session: {e}'
            logger.error(error_msg)
            # self.emailer.send_message(error_msg)
            exit(1)

    async def run(self) -> None:
        logger.info('Starting auto-renewer')
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.config['ENV'] != 'dev', slow_mo=0)
            self.page = await browser.new_page(base_url=self.config['LIBRARY_URL'])
            try:
                await self.__log_in()
                await self.__renew_books()
                await self.__log_out()

            except Exception as e:
                logger.error('Run unsuccessful. %s', e)

            finally:
                await browser.close()

    async def __log_in(self) -> None:
        logger.info('Logging in')
        try:
            await self.page.goto('/user/login')
            # Decline cookies if button on page
            decline_cookies_button = self.page.locator('#rcc-decline-button')
            if await decline_cookies_button.is_visible():
                await decline_cookies_button.click()
            # Fill username field
            user_name_input = self.page.locator('#bNumber')
            await user_name_input.fill(self.config['USER_NAME'])
            # Fill password field
            user_password_input = self.page.locator('#pin')
            await user_password_input.fill(self.config['PASSWORD'])
            # Click login button
            await self.page.locator('button:has-text("Login")').click()

        except Exception as e:
            error_msg = f'Failed to log in: {e}'
            logger.error(error_msg)
            # self.emailer.send_message(error_msg)
            raise Exception from e

    async def __renew_books(self) -> list[LibraryBook]:
        current_holds = await self.__books_from_table()
        books_due = get_books_due(current_holds)
        if books_due:
            logger.info(f'Attempting to renew {len(books_due)} books')
            try:
                await self.page.locator('button:has-text("Renew all")').click()
                await self.page.locator('button:has-text("Renew Selected")').click()
                renewed_books = current_holds
                return renewed_books

            except Exception as e:
                error_msg = f'Failed to renew books: {e}'
                logger.error(error_msg)
                # self.emailer.send_message(error_msg)
                raise Exception from e

        else:
            logger.info(f'No books are due')

        return []

    async def __books_from_table(self) -> list[LibraryBook]:
        logger.info('Collecting information on current holds')
        await self.page.wait_for_load_state("networkidle")
        try:
            table = self.page.locator('table')
            await expect(table).to_be_visible(timeout=10000)

            table_body = table.locator('tbody')
            table_rows = await table_body.locator('tr').all()

            books = []
            for row in table_rows:
                # Select all rows within the table
                row_cells = await row.locator('td').all()
                book = LibraryBook(
                    title=await row_cells[1].inner_text(),
                    author=await row_cells[2].inner_text(),
                    due_date=await row_cells[4].inner_text(),
                    times_renewed=await row_cells[3].inner_text()
                )
                books.append(book)

            return books

        except Exception as e:
            error_msg = f'Failed to get books from table: {e}'
            logger.error(error_msg)
            raise Exception from e

    async def __log_out(self) -> None:
        logger.info('Logging out')
        try:
            # Open user menu
            await self.page.get_by_title('Show User Account submenu').click()
            user_menu = self.page.locator('#user-menu')
            # Click logout button
            await user_menu.locator('button:has-text("Logout")').click()

        except Exception as e:
            error_msg = f'Failed to log out: {e}'
            logger.error(error_msg)
            # self.emailer.send_message(error_msg)
            raise Exception from e
