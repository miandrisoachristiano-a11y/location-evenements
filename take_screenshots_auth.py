import os
from playwright.sync_api import sync_playwright

BASE_URL = "http://localhost:8000"
CAPTURE_DIR = "e:/PROJECT_LICENCE/captures_memoire"

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def main():
    ensure_dir(CAPTURE_DIR)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Create a new context so we can manage cookies (login sessions)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()
        
        try:
            print("--- ADMIN SCREENSHOTS ---")
            page.goto(f"{BASE_URL}/admin-login/")
            page.wait_for_timeout(500)
            
            # Fill login form
            page.fill("input[name='username']", "admin_screenshot")
            page.fill("input[name='password']", "admin_password123")
            page.click("button[type='submit']")
            page.wait_for_load_state('networkidle')
            page.wait_for_timeout(1000)
            
            # Now we should be logged in as admin
            print("Capturing Admin Dashboard")
            page.goto(f"{BASE_URL}/admin-dashboard/")
            page.wait_for_timeout(1000)
            page.screenshot(path=os.path.join(CAPTURE_DIR, "6_admin_dashboard.png"))
            
            print("Capturing Manage Events (CRUD)")
            page.goto(f"{BASE_URL}/admin-dashboard/events/")
            page.wait_for_timeout(1000)
            page.screenshot(path=os.path.join(CAPTURE_DIR, "7_manage_events.png"))
            
            print("Capturing Manage Users (CRUD)")
            page.goto(f"{BASE_URL}/admin-dashboard/users/")
            page.wait_for_timeout(1000)
            page.screenshot(path=os.path.join(CAPTURE_DIR, "8_manage_users.png"))
            
            # Clear cookies to logout
            context.clear_cookies()
            
            print("--- USER SCREENSHOTS ---")
            page.goto(f"{BASE_URL}/login/") # or /accounts/login/
            page.wait_for_timeout(500)
            try:
                page.fill("input[name='username']", "user_screenshot")
                page.fill("input[name='password']", "user_password123")
                page.click("button[type='submit']")
                page.wait_for_load_state('networkidle')
                page.wait_for_timeout(1000)
            except Exception as e:
                print("Login using /login/ failed, trying /accounts/login/", e)
                page.goto(f"{BASE_URL}/accounts/login/")
                page.fill("input[name='username']", "user_screenshot")
                page.fill("input[name='password']", "user_password123")
                page.click("button[type='submit']")
                page.wait_for_load_state('networkidle')
                page.wait_for_timeout(1000)
            
            print("Capturing Panier")
            page.goto(f"{BASE_URL}/panier/")
            page.wait_for_timeout(1000)
            page.screenshot(path=os.path.join(CAPTURE_DIR, "9_panier.png"))
            
            print("Capturing User Profile / User Dashboard")
            page.goto(f"{BASE_URL}/profile/")
            # Just in case profile redirects to user-dashboard or similar
            page.wait_for_timeout(1000)
            page.screenshot(path=os.path.join(CAPTURE_DIR, "10_user_profile.png"))
            
        except Exception as e:
            print("Error capturing pages:", e)
        finally:
            browser.close()
            
    print("Authenticated captures completed.")

if __name__ == "__main__":
    main()
