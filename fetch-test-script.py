import httpx
import browser_cookie3

URL = "https://janitorai.com/hampter/chats/2137670492"

# ========================================
# получаем cookies из Chrome
# ========================================
print("[LOG] Loading cookies from Chrome...")

cookies = browser_cookie3.chrome(domain_name="janitorai.com")

print("[LOG] Cookies loaded")

# ========================================
# headers как у браузера
# ========================================
headers = {
    "Accept": "application/json, text/plain, */*",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6IkRhOW1BcjVxbkZmQWF2TisiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL21jbXp4dHpvbW1wbnhreW5kZGJvLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiJjYmJjOTU3Mi0xMDllLTRlMGEtYmU2Zi1lYmE2OTAyZmFmNjIiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzczNDMyMjAzLCJpYXQiOjE3NzM0MzA0MDMsImVtYWlsIjoidHVwZXlrb21hQGdtYWlsLmNvbSIsInBob25lIjoiIiwiYXBwX21ldGFkYXRhIjp7ImJldGEiOnRydWUsInByb3ZpZGVyIjoiZ29vZ2xlIiwicHJvdmlkZXJzIjpbImdvb2dsZSJdfSwidXNlcl9tZXRhZGF0YSI6eyJhbGxvd19tb2JpbGVfbnNmdyI6dHJ1ZSwiYXZhdGFyX3VybCI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0lXckE1eXIwVlc5WHVDbFZRZmRLS3F0S1pndk9vMXhjZm43S1ZyTTBsdFoxNl8zNXlsPXM5Ni1jIiwiY3JlYXRlZF9hdCI6IjE2ODY3MzAyMzAzNDciLCJlbWFpbCI6InR1cGV5a29tYUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZnVsbF9uYW1lIjoiTWlsYW5hIFR1cGV5a28iLCJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJuYW1lIjoiTWlsYW5hIFR1cGV5a28iLCJwaG9uZV92ZXJpZmllZCI6ZmFsc2UsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NJV3JBNXlyMFZXOVh1Q2xWUWZkS0txdEtaZ3ZPbzF4Y2ZuN0tWck0wbHRaMTZfMzV5bD1zOTYtYyIsInByb3ZpZGVyX2lkIjoiMTA2MjYzMDQ5ODUzNTk3MTE0ODk3Iiwic3ViIjoiMTA2MjYzMDQ5ODUzNTk3MTE0ODk3In0sInJvbGUiOiJhdXRoZW50aWNhdGVkIiwiYWFsIjoiYWFsMSIsImFtciI6W3sibWV0aG9kIjoib2F1dGgiLCJ0aW1lc3RhbXAiOjE3NzAwNTExMzZ9XSwic2Vzc2lvbl9pZCI6IjEwYjIyYjYzLTBjMWItNDgwMy1iYmU0LTMxYTY3YjJiN2UxYiIsImlzX2Fub255bW91cyI6ZmFsc2V9.dzmpa1FpsfiJK1Kqt5qF8_vEwEzoNrlBw8povh1pFZQ",
    "Referer": "https://janitorai.com/chats/2137670492",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
    "x-app-version": "7.9.1",
}

print("[LOG] Sending request...")
print("[LOG] URL:", URL)

# ========================================
# запрос
# ========================================
with httpx.Client(cookies=cookies, timeout=30) as client:
    response = client.get(URL, headers=headers)

print("[LOG] Status:", response.status_code)

if response.status_code != 200:
    print("[LOG] Error response:")
    print(response.text[:1000])
else:
    print("[LOG] Success")
    print(response.text[:500])