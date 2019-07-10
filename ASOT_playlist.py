from bs4 import BeautifulSoup
import requests
import json

source = requests.get('https://www.astateoftrance.com/episodes/').text

soup = BeautifulSoup(source, 'lxml')

article = soup.find('article', class_='col w20 first news')

ep_source = article.find('a')['href']
ep_title = article.find('a')['title'].split(' ')
episode_num = ep_title[len(ep_title) - 1]

source = requests.get(ep_source).text
soup = BeautifulSoup(source, 'lxml')

song_list = soup.find('div', class_='playlist col first w60').ol

ep_songlist = []


#Remove Record label from the song name
def remove_label(song):
	song_only = song.split('[')
	return song_only[0].strip()

#Remove PICKS OF THE WEEK
for song in song_list.find_all('li'):
	song_details = {}
	if song.strong.text.find(':') != -1:
		feature_song = song.strong.text.split(': ')
		artist = feature_song[1]
	else:
		artist = song.strong.text

	#multiple artits
	multilist = ['&',' x ','feat.',',']
	main_artist = artist
	for x in multilist:
		if x in artist:
			artist_split = artist.split(x)
			main_artist = artist_split[0]
		else:
			pass
	
	print(main_artist)
	_song = song.text

	#Ensure split on En dash
	_song = _song.replace("\u2013", "-")
	split_text = _song.split('-',1)
	song_label = split_text[len(split_text) -1]

	song_name = remove_label(song_label)


	#Find Remix name
	if song_name.find('(') != -1:
		peri = song_name.split('(')
		song_name = peri[0].strip()
		#check for mashup
		if song_name.find('-') != -1:
			vs_split = song_name.split('-')
			song_name = vs_split[len(vs_split)-1]
			song_name = song_name.strip()
		else:
			pass
		if 'Remix' in peri[1]:
			remix_name = peri[1].replace('Remix)','')
			remix_name = remix_name.strip()
		else:
			remix_name = None
	else:
		if song_name.find('-') != -1:
			vs_split = song_name.split('-')
			song_name = vs_split[len(vs_split)-1]
			song_name = song_name.strip()
		else:
			pass
		remix_name = None

	song_details['artist'] = main_artist
	song_details['song'] = song_name
	song_details['remix'] = remix_name
	ep_songlist.append(song_details)

print(ep_songlist)

