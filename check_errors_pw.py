import sys
from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        page.goto("http://localhost:8000/login/")
        try:
            page.fill("input[name='username']", "admin")
            page.fill("input[name='password']", "admin123")
            page.click("button[type='submit']")
            page.wait_for_load_state("networkidle")
        except Exception as e:
            print("Login error:", e)
            
        page.goto("http://localhost:8000/")
        content = page.content()
        if "Exception Value:" in content:
            import re
            m = re.search(r'Exception Value:.*?<pre>(.*?)</pre>', content, re.DOTALL)
            if m:
                print("TEMPLATE ERROR:", m.group(1))
        else:
            print("No template error on /")
            
        # check /calendario/
        page.goto("http://localhost:8000/calendario/")
        content = page.content()
        if "Exception Value:" in content:
            import re
            m = re.search(r'Exception Value:.*?<pre>(.*?)</pre>', content, re.DOTALL)
            if m:
                print("TEMPLATE ERROR ON /calendario/:", m.group(1))
        else:
            print("No template error on /calendario/")
            
        browser.close()

if __name__ == "__main__":
    main()
