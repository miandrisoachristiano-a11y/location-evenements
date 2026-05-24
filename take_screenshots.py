import os
import time
from playwright.sync_api import sync_playwright

BASE_URL = "http://localhost:8000"
CAPTURE_DIR = "e:/PROJECT_LICENCE/captures_memoire"

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def main():
    ensure_dir(CAPTURE_DIR)
    print("Capturing screenshots in", CAPTURE_DIR)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": 1280, "height": 800})
        
        try:
            print("1. Accueil")
            page.goto(f"{BASE_URL}/")
            page.wait_for_timeout(1000)
            page.screenshot(path=os.path.join(CAPTURE_DIR, "1_accueil.png"))
            
            print("2. Inscription / Connexion")
            page.goto(f"{BASE_URL}/accounts/login/")
            page.wait_for_timeout(1000)
            page.screenshot(path=os.path.join(CAPTURE_DIR, "2_connexion.png"))
            
            print("3. Inscription")
            page.goto(f"{BASE_URL}/register/")
            page.wait_for_timeout(1000)
            page.screenshot(path=os.path.join(CAPTURE_DIR, "3_inscription.png"))
            
            print("4. Admin")
            page.goto(f"{BASE_URL}/admin-login/")
            page.wait_for_timeout(1000)
            page.screenshot(path=os.path.join(CAPTURE_DIR, "5_admin_login.png"))
            
        except Exception as e:
            print("Error capturing pages:", e)
        finally:
            browser.close()
            
    print("Captures completed.")

if __name__ == "__main__":
    main()
