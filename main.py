from facebook import Page


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
p = Page('293771760745242', user_agent)

print(p.get_name())
print(p.get_likes())
print(p.get_address())
print(p.is_verified())
