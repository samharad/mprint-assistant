import requests
import json
import subprocess

# jar = requests.cookies.RequestCookieJar()
# jar.set('')
# getCooks = requests.post('https://weblogin.umich.edu', data={'login':'', 'password':''})
# print getCooks.text
# print requests.utils.dict_from_cookiejar(getCooks.cookies)

s = requests.Session()
res = s.get('https://weblogin.umich.edu/')
for cookie in res.cookies:
	print (cookie.name, cookie.value)
print res.headers
# print cooks
res2 = s.post('https://weblogin.umich.edu/', data={'login':'', 'password':''})
print res2.headers
for cookie in res2.cookies:
	print (cookie.name, cookie.value)
print 'here'
# print cooks

queues = s.get('https://mprint.umich.edu/api/queues?all')
print queues.text