from django.shortcuts import render
import json
import requests
import urllib.request
import wikipedia



querystring=""
url = "https://genius.p.rapidapi.com/search"
headers = {
    'x-rapidapi-key': "c82d01a24fmsh6fbca4f9e9629bbp10beddjsn379d4221dc0e",
    'x-rapidapi-host': "genius.p.rapidapi.com"
    }

def home(request):
    search_term=" "
    
    if request.method=='GET':
        search_term = request.GET.get('search_box', "")             
        response = give_response(search_term)

        try:
            artist_id=response['response']['hits'][0]['result']['primary_artist']['id']
                      
        except:
            pass    
        try:

            [facebook_name,instagram_name,twitter_name,genius_url,alternate_name]=social_media(artist_id)
            alternate_name="Also known as \'"+ alternate_name+"\'" 
        except:
            [facebook_name,instagram_name,twitter_name,genius_url,alternate_name]=["","","","",""]

        songnames=[]
        thumbnails=[]
        pageviews=[]
        page0,page1,page2,page3="","","",""
        song0,song1,song2,song3="","","",""
        ans=response['response']['hits']
        
        try:
            for i in range(len('hits')):
                song=ans[i]['result']
                by_title=song['full_title'].split('by')
                title=by_title[0]
                thumbnail=song['song_art_image_thumbnail_url']             
                pageview=song['stats']['pageviews']

                songnames.append(title)
                thumbnails.append(thumbnail)
                pageviews.append(pageview)
        except:
            pass
        

        try:

            song0,song1,song2,song3=songnames[0],songnames[1],songnames[2],songnames[3]
            page0,page1,page2,page3=pageviews[0],pageviews[1],pageviews[2],pageviews[3]
        except:
            song0,song1,song2,song3="","","",""
            page0,page1,page2,page3="","","",""               
                           
        
        try:
            if " " in search_term:
                query=search_term.replace(" ","_")
                wiki_info=wikipedia.summary(query,sentences=4,auto_suggest=False)
                
            else:
                wiki_info=wikipedia.summary(search_term,sentences=4) 
        except:
            wiki_info=""
        
    
        
        
        try:
            context={'songnames':songnames,'search_term':search_term,'facebook_name':facebook_name,
            'instagram_name':instagram_name,'twitter_name':twitter_name,'pageviews':pageviews,
            'wiki_info':wiki_info,'genius_url':genius_url,'alternate_name':alternate_name,
            'page0':page0,'page1':page1,'page2':page2,'page3':page3,
            'song0':song0,'song1':song1,'song2':song2,'song3':song3}
            
            
            return render(request,'home.html',context)

        except:
            return(render(request,'home.html'))   





def give_response(search_term):
        querystring = {"q":search_term}
        response = requests.request("GET", url, headers=headers, params=querystring).json()
        return(response)


def social_media(artist_id):
    url = "https://genius.p.rapidapi.com/artists/" + str(artist_id)
    response = requests.request("GET", url, headers=headers).json()
    
    alternate_name=response['response']['artist']['alternate_names'][0]
    facebook_name=response['response']['artist']['facebook_name']
    instagram_name=response['response']['artist']['instagram_name']
    twitter_name=response['response']['artist']['twitter_name']
    genius_url=response['response']['artist']['twitter_name']
       
    return([facebook_name,instagram_name,twitter_name,genius_url,alternate_name])







