import mysql.connector
from contextlib import contextmanager
import sys
from datetime import datetime
from math import ceil
from fuzzywuzzy import fuzz
from random import Random
class Engine():
    
    def __init__(self):
        self.ITEM_PER_PAGE = 40
        self.SIMILAR_PER_PAGE = 20
        self.SEARCH_ITEMS = 10
        self.stop_words = ['dub','movie','anime','the','season','1st','3rd','2nd','4th','5th','sub','movie:','first','second','third','fourth'] 
    @contextmanager
    def open_db_connection(self, commit=False):
        connection = mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        passwd="",
        database='anime_db'
        )
        print(connection.is_connected())
        cursor = connection.cursor(dictionary=True)
        try:
            yield cursor
        except Exception as err:
            error, = err.args
            sys.stderr.write(error)
            cursor.execute("ROLLBACK")
            raise err
        else:
            if commit:
                cursor.execute("COMMIT")
            else:
                cursor.execute("ROLLBACK")
        finally:
            connection.close()
            
    def get_episode_homePage(self,max):
        with self.open_db_connection() as cursor:
            # DB View : get_latest_episodes
            cursor.execute("select * from get_latest_episodes LIMIT %s",[max])
            episodes = self.concatenate_genres(cursor.fetchall())
            return episodes
    def concatenate_genres(self,episodes): 
        with self.open_db_connection() as cursor:
            for episode in episodes:
                cursor.execute("SELECT * from anime_genre where id_anime = %s",[episode['id']])
                episode['genres'] = ', '.join([genre['id_genre'] for genre in cursor.fetchall()])
        return episodes
            
    def get_onGoing(self,max):
        with self.open_db_connection() as cursor:
            cursor.execute('SELECT * FROM animes  WHERE status = \'RELEASING\' ORDER BY averageScore LIMIT {max}'.format(max=max))
            return cursor.fetchall()
    def check_slug(self,slug):
        with self.open_db_connection() as mycursor:
            sg          = '-'.join(slug.split('-')[:-1])
            id_api      = slug.split('-')[-1]
            response    = {}
            mycursor.execute("SELECT * FROM animes WHERE slug = '{slug}' AND id_api = '{id_api}' "
                            .format(slug   =   sg,
                                    id_api =   id_api))
            row         = mycursor.fetchone()
            if mycursor.rowcount == -1:
                #NotFound
                return {}
            else:
                mycursor.execute("SELECT * FROM episodes WHERE id_anime = %s ",[row['id']])
                response['info'] = row                
                response['episodes'] = mycursor.fetchall()
                mycursor.execute("SELECT id_genre FROM anime_genre WHERE id_anime = %s ",[row['id']])
                response['genres'] = mycursor.fetchall()
                return response
    def get_episode_servers(self,episode):

            #sg      = '-'.join(splits[:-])
        with self.open_db_connection() as mycursor:
            response                =   {}
            # get episode
            mycursor.execute("SELECT * FROM episodes WHERE id = %s",[episode])
            response['episode']     =   mycursor.fetchone()
            response['episode']['links'] = [{'server':i+1,'link':link} for i,link in enumerate(response['episode']['links'].split('|'))]
            try:
                response['episode']['episodeDisplay'] = int(response['episode']['episode'])
            except:
                response['episode']['episodeDisplay'] = response['episode']['episode']
            current_index           =   response['episode']['index_ep']
            # get anime url
            id_anime = response['episode']['id_anime']
            mycursor.execute("SELECT id_api,slug,name,id FROM animes WHERE id = %s",[id_anime])
            response['anime_url']  = mycursor.fetchone()
            index_last,index_next = (None,None)
            # get last episode
            if current_index > 1:
                mycursor.execute("SELECT episode FROM episodes WHERE index_ep = %s AND id_anime = %s",[current_index - 1,id_anime])
                index_last = mycursor.fetchone()['episode']
            # get next episode
            mycursor.execute("SELECT episode FROM episodes WHERE index_ep = %s AND id_anime = %s",[current_index + 1,id_anime])
            #print(mycursor.fetchone())
            #print('-----------{}'.format(rowscount))
            rows = mycursor.fetchall()
            if len(rows) >= 1:
                index_next = rows[0]['episode']
            response['last'] = index_last
            response['next'] = index_next
            response['loweredName'] = ' '.join(response['anime_url']['slug'].split('-'))
            return response

    def get_anime_list(self,page):
        if page > 0:
            page -= 1
        offset = page * self.ITEM_PER_PAGE
        with self.open_db_connection() as mycursor:
            mycursor.execute("SELECT * FROM animes order by start_date DESC LIMIT %s,%s",[offset,self.ITEM_PER_PAGE])
            print('--------------- {}'.format(mycursor._executed))
            return mycursor.fetchall()
        
        
    def get_dubbed_anime(self,page):
        if page > 0:
            page -= 1
        offset = page * self.ITEM_PER_PAGE
        with self.open_db_connection() as mycursor:
            mycursor.execute("SELECT * FROM animes WHERE name LIKE '%(Dub)' order by start_date DESC LIMIT %s,%s",[offset,self.ITEM_PER_PAGE])
            print('--------------- {}'.format(mycursor._executed))
            return mycursor.fetchall()
    
    def get_tvs(self,page):
        if page > 0:
            page -= 1
        offset = page * self.ITEM_PER_PAGE
        with self.open_db_connection() as mycursor:
            mycursor.execute("SELECT * FROM animes WHERE format = 'TV' or format = 'TV_SHORT' order by start_date DESC LIMIT %s,%s",[offset,self.ITEM_PER_PAGE])
            print('--------------- {}'.format(mycursor._executed))
            return mycursor.fetchall()
    '''
    def get_ongoing(self,page):
        if page > 0:
            page -= 1
        offset = page * self.ITEM_PER_PAGE
        with self.open_db_connection() as mycursor:
            mycursor.execute("SELECT * FROM animes  WHERE status = \'RELEASING\' order by start_date DESC LIMIT %s,%s",[offset,self.ITEM_PER_PAGE])
            print('--------------- {}'.format(mycursor._executed))
            return mycursor.fetchall()
    '''
    def get_popular(self,page):
        if page > 0:
            page -= 1
        offset = page * self.ITEM_PER_PAGE
        with self.open_db_connection() as mycursor:
            mycursor.execute("SELECT * FROM animes order by popularity DESC LIMIT %s,%s",[offset,self.ITEM_PER_PAGE])
            print('--------------- {}'.format(mycursor._executed))
            return mycursor.fetchall()   
        
    def get_total_pages(self,type):
        with self.open_db_connection() as mycursor:
            if type == 'animes':
                mycursor.execute("SELECT count(*) as count FROM animes ")
            elif type == 'dubbed':
                mycursor.execute("SELECT count(*) as count FROM animes WHERE name LIKE '%(Dub)'")
            elif type == 'tv':
                mycursor.execute("SELECT count(*) as count FROM animes WHERE format = 'TV' or format = 'TV_SHORT'")
            elif type == 'popular':
                mycursor.execute("SELECT count(*) as count FROM animes")
                
            return ceil(mycursor.fetchone()['count'] / self.ITEM_PER_PAGE)

    def get_random(self):
        rd = Random()
        with self.open_db_connection() as cursor:
            cursor.execute("SELECT id_api,slug FROM animes")
            animes = cursor.fetchall()
            return animes[rd.randint(0,len(animes)-1)]
    def get_similar_animes(self,slug,id,genres):
        slug = ' '.join([word for word in slug.split('-') if word not in self.stop_words])
        with self.open_db_connection() as cursor:
            genre_condition = ["id_genre = '{}'".format(genre['id_genre']) for genre in genres]
            cursor.execute("SELECT id, slug FROM animes,anime_genre WHERE id != %s and id = id_anime and ({}) ".format(' OR '.join(genre_condition)),[id])
            print(cursor._executed)
            animes = cursor.fetchall()
            if (len(animes) == 0):
                return []
            scores = [{'id':anime['id'],
                       'score':fuzz.ratio(slug,' '.join([word for word in anime['slug'].split('-') if word not in self.stop_words]))}
                            for anime in animes]
            ids = ['\''+anime['id']+'\'' for anime in sorted(scores,key=lambda i:i['score'],reverse=True)[:self.SIMILAR_PER_PAGE]]
            cursor.execute("SELECT name,slug,id_api,coverImage FROM animes WHERE id in ({})".format(','.join(ids)))
            return cursor.fetchall()
    def search(self,keyword):
        
        keyword = ' '.join([word for word in keyword.lower().split('-') if word not in self.stop_words])
        with self.open_db_connection() as cursor:
            cursor.execute("SELECT id, slug FROM animes")
            animes = cursor.fetchall()
            scores = [{'id':anime['id'],
                       'score':fuzz.ratio(keyword,' '.join([word for word in anime['slug'].split('-') if word not in self.stop_words]))}
                            for anime in animes]
            ids = ['\''+anime['id']+'\'' for anime in sorted(scores,key=lambda i:i['score'],reverse=True)[:self.SEARCH_ITEMS]]
            cursor.execute("SELECT name,slug,id_api,coverImage FROM animes WHERE id in ({})".format(','.join(ids)))
            return cursor.fetchall()