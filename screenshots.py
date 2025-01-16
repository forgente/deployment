import asyncio
import os

from playwright.async_api import async_playwright


anonymous_urls = {
    "login": "https://gitea.com/user/login",
}

login_urls = {
    "home": "https://gitea.com",
    "issues": "https://gitea.com/issues",
    "pull_requests": "https://gitea.com/pulls",
    "milestones": "https://gitea.com/milestones",

    "explore_repos": "https://gitea.com/explore/repos",
    "explore_users":"https://gitea.com/explore/users",
    "explore_orgs":"https://gitea.com/explore/organizations",

    "repo_home": "https://gitea.com/gitea/act_runner",
    
    "repo_commits": "https://gitea.com/gitea/act_runner/commits/branch/main",
    "repo_branches": "https://gitea.com/gitea/act_runner/branches",

    "repo_labels": "https://gitea.com/gitea/act_runner/labels",
    # TODO: act runner does not have milestones
    "repo_milestones": "https://gitea.com/gitea/act_runner/milestones",

    "repo_issues": "https://gitea.com/gitea/act_runner/issues",
    "repo_issue": "https://gitea.com/gitea/act_runner/issues/8",

    "repo_pull_requests": "https://gitea.com/gitea/act_runner/pulls",
    "repo_pull_request": "https://gitea.com/gitea/act_runner/pulls/630",
    "repo_pull_request_file":"https://gitea.com/gitea/act_runner/pulls/630/files",
    "repo_pull_request_commits":"https://gitea.com/gitea/act_runner/pulls/630/commits",

    "repo_actions": "https://gitea.com/gitea/act_runner/actions",
    "repo_actions_run": "https://gitea.com/gitea/act_runner/actions/runs/1000",

    "repo_releases": "https://gitea.com/gitea/act_runner/releases",
    "repo_tags": "https://gitea.com/gitea/act_runner/tags",

    "repo_activity": "https://gitea.com/gitea/act_runner/activity",
    "repo_contributors": "https://gitea.com/gitea/act_runner/activity/contributors",
    "repo_code_frequency": "https://gitea.com/gitea/act_runner/activity/code-frequency",
    "repo_recent_commits": "https://gitea.com/gitea/act_runner/activity/recent-commits",

    "org_home": "https://gitea.com/gitea",

    "user_profile": "https://gitea.com/lunny",
}

async def take_screenshot(page, name, url):
    print(f"Taking screenshot of {name}.png at {url}")
    await page.goto(url, wait_until="networkidle")
    await page.screenshot(path=f'screenshots/{name}.png')

async def main():
    username = os.getenv("BOT_USERNAME")
    password = os.getenv("BOT_PASSWORD")
    if not username or not password:
        raise ValueError("Please provide BOT_USERNAME and BOT_PASSWORD environment variables")

    os.makedirs("screenshots", exist_ok=True)

    async with async_playwright() as p:
        browser = await p.webkit.launch()
        page = await browser.new_page(
            color_scheme="dark",
            viewport={"width": 1920, "height": 1080}
        )

        for name, url in anonymous_urls.items():
            if name == "login":
                # skip login page, we will take screenshot during login
                continue
            await take_screenshot(page, name, url)

        # login
        await take_screenshot(page, "login", anonymous_urls["login"])
        await page.fill("#user_name", username)
        await page.fill("#password", password)
        await page.get_by_role("button", name="Sign In").click()
        await page.wait_for_load_state("domcontentloaded")

        for name, url in login_urls.items():
            await take_screenshot(page, name, url)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
