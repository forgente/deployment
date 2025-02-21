import os

import pytest
from playwright.async_api import Browser
from playwright.async_api import async_playwright


@pytest.mark.asyncio
async def test_install():
    async with async_playwright() as playwright:
        browser = await playwright.webkit.launch()
        await install(browser)
        await browser.close()

async def install(browser: Browser):
    server_host = os.environ.get("SERVER_HOST")

    context = await browser.new_context()
    page = await context.new_page()

    response = await page.goto(server_host)
    assert response.status == 200

    # select db (default is sqlite3)
    db_type = os.getenv("DB_TYPE", "sqlite3")
    db_dropdown = page.locator(".ui.selection.database.type.dropdown").first
    await db_dropdown.click()
    db_type_options = await db_dropdown.get_by_role("option").all()

    found = False
    for db_type_option in db_type_options:
        if await db_type_option.get_attribute("data-value") == db_type:
            await db_type_option.click()
            found = True
            break
    assert found

    # fill db connection info
    if db_type == "sqlite3":
        pass
    elif db_type == "mysql":
        db_host = os.getenv("DB_HOST", "mysql:3306")
        db_user = os.getenv("DB_USER", "root")
        db_passwd = os.getenv("DB_PASSWD", "")
        db_name = os.getenv("DB_NAME", "testgitea")
        await page.locator("#db_host").fill(db_host)
        await page.locator("#db_user").fill(db_user)
        await page.locator("#db_passwd").fill(db_passwd)
        await page.locator("#db_name").fill(db_name)
    elif db_type == "pgsql":
        db_host = os.getenv("DB_HOST", "pgsql:5432")
        db_user = os.getenv("DB_USER", "postgres")
        db_passwd = os.getenv("DB_PASSWD", "postgres")
        db_name = os.getenv("DB_NAME", "testgitea")
        db_schema = os.getenv("DB_SCHEMA", "gtestschema")
        await page.locator("#db_host").fill(db_host)
        await page.locator("#db_user").fill(db_user)
        await page.locator("#db_passwd").fill(db_passwd)
        await page.locator("#db_name").fill(db_name)
        await page.locator("#db_schema").fill(db_schema)
    elif db_type == "mssql":
        db_host = os.getenv("DB_HOST", "mssql:1433")
        db_user = os.getenv("DB_USER", "sa")
        db_passwd = os.getenv("DB_PASSWD", "MwantsaSecurePassword1")
        db_name = os.getenv("DB_NAME", "testgitea")
        await page.locator("#db_host").fill(db_host)
        await page.locator("#db_user").fill(db_user)
        await page.locator("#db_passwd").fill(db_passwd)
        await page.locator("#db_name").fill(db_name)

    # fill admin user info
    await page.locator("details").filter(has=page.locator("#admin_name")).click()
    await page.locator("#admin_name").fill("giteaadmin")
    await page.locator("#admin_email").fill("admin@example.com")
    await page.locator("#admin_passwd").fill("Test123456789")
    await page.locator("#admin_confirm_passwd").fill("Test123456789")
    await page.get_by_role("button", name="Install Gitea").click(timeout=60000) # use a long timeout to wait for the install

    # wait for the install
    await page.wait_for_load_state("networkidle")

    await browser.close()
