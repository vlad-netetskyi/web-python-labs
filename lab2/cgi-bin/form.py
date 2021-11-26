import cgi
import html
import http.cookies
import os

cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
count = cookie.get("count")

if count is None:
    print("Set-cookie: count=0 httponly")
else:
    print(f"Set-cookie: count={str(int(count.value) + 1)} httponly")

form = cgi.FieldStorage()
first_name = form.getfirst("TEXT_1", "не задано")
last_name = form.getfirst("TEXT_2", "не задано")
adult = form.getfirst("adult", "не задано")
first_name = html.escape(first_name)
last_name = html.escape(last_name)
adult = html.escape(adult)

print("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Обробка данних форм</title>
        </head>
        <body>""")

print("<h1>Обработка данних форм!</h1>")
print("<p>First name: {}</p>".format(first_name))
print("<p>Last name: {}</p>".format(last_name))
print("Is adult:", "yes" if adult == "on" else "no")

print("""</body>
        </html>""")
