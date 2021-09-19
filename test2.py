import requests

#Get the link or url

url = 'https://www.google.com/imgres?imgurl=https%3A%2F%2Ficatcare.org%2Fapp%2Fuploads%2F2018%2F07%2FThinking-of-getting-a-cat.png&imgrefurl=https%3A%2F%2Ficatcare.org%2Fadvice%2Fthinking-of-getting-a-cat%2F&tbnid=0V922RrJgQc9SM&vet=12ahUKEwjfqNiXkfryAhWIxCoKHVo4DjwQMygAegUIARDLAQ..i&docid=5qEHfJOysK_DwM&w=1200&h=600&q=cats&hl=en&ved=2ahUKEwjfqNiXkfryAhWIxCoKHVo4DjwQMygAegUIARDLAQ'
r = requests.get(url, allow_redirects=True)

#Save the content with name.

open('facebook.ico', 'wb').write(r.content)
