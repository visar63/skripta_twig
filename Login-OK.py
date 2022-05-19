import requests
import re

url = 'https://www.videdressing.co.uk/product/sell.html'

resp = requests.get(url)
if resp.status_code == 200:
    # print (resp.text)
    print(resp.request.headers)
    print("\n\n")
    print(resp.headers)
    with open('page1.html', 'w', encoding='utf-8') as aa:
        aa.write(resp.text)

    csrf_pttr = re.search(r'<input name="no_csrf_login_submit_post" type="hidden" value="([^"]+)"', resp.text)
    if csrf_pttr:
        csrf = csrf_pttr.group(1)
        print (f'CSRF: {csrf}')

        url2 = "https://www.videdressing.co.uk/user/login.html"

        querystring = {"redirect":"product/sell"}

        payload = f"login_submit_post=Login&mail=arbliki22%40gmail.com&no_csrf_login_submit_post=b14db596960bb5e9509610e6c0b78dd6&pass=Ar-bliki123%23"
        headers = {
            'sec-ch-ua': "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"101\", \"Google Chrome\";v=\"101\"",
            'sec-ch-ua-mobile': "?0",
            'sec-ch-ua-platform': "\"Windows\"",
            'upgrade-insecure-requests': "1",
            'content-type': "application/x-www-form-urlencoded",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "navigate",
            'sec-fetch-user': "?1",
            'sec-fetch-dest': "document",
            'cache-control': "no-cache",
            'cookie': 'didomi_token=eyJ1c2VyX2lkIjoiMTgwZGMxN2YtNTg4ZC02NThiLWIxNWMtNmJmMzIxYzY1NmRmIiwiY3JlYXRlZCI6IjIwMjItMDUtMTlUMTE6MzM6MjEuNzEwWiIsInVwZGF0ZWQiOiIyMDIyLTA1LTE5VDExOjMzOjIxLjcxMFoiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiZ29vZ2xlIiwiYzpyb2NreW91IiwiYzpwdWJvY2Vhbi1iNkJKTXRzZSIsImM6cnRhcmdldC1HZWZNVnlpQyIsImM6c2NoaWJzdGVkLU1RUFhhcXloIiwiYzpncmVlbmhvdXNlLVFLYkdCa3M0IiwiYzpyZWFsemVpdGctYjZLQ2t4eVYiLCJjOnNhbGVjeWNsZSIsImM6eW9ybWVkaWFzLXFuQldoUXlTIiwiYzpzYW5vbWEiLCJjOnJhZHZlcnRpcy1TSnBhMjVIOCIsImM6cXdlcnRpemUtemRuZ0UyaHgiLCJjOnJldmxpZnRlci1jUnBNbnA1eCIsImM6cmVzZWFyY2gtbm93IiwiYzp3aGVuZXZlcm0tOFZZaHdiMlAiLCJjOmFkbW90aW9uIiwiYzp0aGlyZHByZXNlLVNzS3dtSFZLIiwiYzpkaWRvbWkiLCJjOmpxdWVyeSIsImM6YWItdGFzdHkiLCJjOmFkbW9iIiwiYzpsYmNmcmFuY2UtR1RZTHl4TWMiLCJjOmdvb2dsZWFuYS1rN3hUUThqRCIsImM6aWFkdml6ZWMtWTl6Ym53ZkgiXX0sInB1cnBvc2VzIjp7ImVuYWJsZWQiOlsiZXhwZXJpZW5jZXV0aWxpc2F0ZXVyIiwibGJjX2F1ZGllbmNlX21lYXN1cmUiXX0sInZlbmRvcnNfbGkiOnsiZW5hYmxlZCI6WyJnb29nbGUiLCJjOmxiY2ZyYW5jZS1HVFlMeXhNYyJdfSwidmVyc2lvbiI6MiwiYWMiOiJETFdBNkFFSUFJd0FXUUItZ0dGQVNTQWtzQ0FZRVNRSlNBY1FBNmNCMVlFVkFJNXdTVGdsWUJONENoRUZGb0s1d1dDZ3R2QmNZQzVZR0F3TUlnWW1neTFBLkRMV0E0QUVJQUl3QV9RRENnSkpBU1dCQU1DSklFcEFPSUFkT0E2c0NLZ0VjNEpKd1NzQW04QlFpQ2kwRmM0TEJRVzNndU1CY3NEQVlHRVFNVFFaYWdBQUEifQ==; euconsent-v2=CPZN1UAPZN1UAAHABBENCPCgAP_AAH_AAAqIIwtf_X__b3_j-_5_f_t0eY1P9_7__-0zjhfdt-8N3f_X_L8X42M7vF36pq4KuR4Eu3LBIQdlHOHcTUmw6okVrzPsbk2cr7NKJ7PEmnMbO2dYGH9_n93TuZKY7_____7z_v-v_v____f_7-3f3__5_3_--_e_V_99zbn9_____9nP___9v-_9_________gjAASYal5AF2JY4Mm0aRQogRhWEh1AoAKKAYWiKwgdXBTsrgJ9QQsAEAqAjAiBBiCjBgEAAgEASERASAHggEQBEAgABAAqAQgAI2AQWAFgYBAAKAaFiBFAEIEhBkQERymBARIlFBPZWIJQd7GmEIdZYAUCj-ioQESgBAsDISFg5jgCQEuFkgWYoXyAEYIUAAAAA.f_gAD_gAAAAA; _ALGOLIA=anonymous-64d8b194-33c0-4b54-bea6-5914d4da8b85; ga_id=UA-11714091-23; product_views=p12565251-; segment=1; identifier=ff698baa4db24c6cd990f53c631cb3f70135ad6d4fd527706cb00649f4d3a961; VDIDANON=%7B%22data%22%3A%7B%22cart%22%3A%7B%22country%22%3A%22GB%22%2C%22currency%22%3A%22EUR%22%2C%22items%22%3A%5B%5D%2C%22buyable_options%22%3A%5B%5D%7D%2C%22Vd_Form_Element_Hash%22%3A%7B%22no_csrf_submit_post%22%3A%2255336e8aac5ee6f50151b468c26a941b%22%2C%22no_csrf_login_submit_post%22%3A%22b14db596960bb5e9509610e6c0b78dd6%22%2C%22no_csrf_submit_inscription_post%22%3A%228725e8f18b0451bc55a279ac63d99264%22%2C%22no_csrf_create_store_submit_post%22%3A%221410bce57e8b89998572ebb9dab3ee51%22%7D%7D%2C%22hash%22%3A%2282d4e76ee1478bf803a39b19c765d8f8c3d215f6%22%7D'
            }
        try:
            response = requests.request("POST", url2, data=payload, headers=headers, params=querystring)

            print(f'\nlength: {len(response.text)}\n')
            with open('page2.html', 'w', encoding='utf-8') as bb:
                bb.write(response.text)
        except Exception as e:
            print (e)
else:
    print (f'Error: {resp.status_code}')