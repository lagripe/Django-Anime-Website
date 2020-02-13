import mysql.connector
from contextlib import contextmanager
import sys
from datetime import datetime
class Engine():
    '''
    def __init__(self):
        self.mydb = mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        passwd="",
        database='anime_db'
        )
        print('connected mysql : {}'.format(self.mydb.is_connected()))
    ''' 
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
            cursor.execute('''SELECT * FROM animes
                                '''.format(max=max))
            return cursor.fetchall()
        ''' 
        mycursor = self.mydb.cursor(dictionary=True)
        mycursor.execute('SELECT name,id,coverImage,description FROM animes'.format(max=max))
        return mycursor.fetchall()
        '''
    def get_onGoing(self,max):
        with self.open_db_connection() as cursor:
            cursor.execute('SELECT * FROM animes  WHERE status = \'RELEASING\' ORDER BY averageScore LIMIT {max}'.format(max=max))
            return cursor.fetchall()
        '''
        mycursor = self.mydb.cursor(dictionary=True)
        mycursor.execute('SELECT name,id,coverImage,description FROM animes  WHERE status = \'RELEASING\' ORDER BY popularity LIMIT {max}'.format(max=max))
        return mycursor.fetchall()
        '''
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
    def get_episode_servers(self,episode_slug):
        splits      =   episode_slug.split('-')
        if len(splits) < 3:
            return {}
        else:
            episode     =   splits[-1]
            id_anime    =   splits[-2]
            #sg      = '-'.join(splits[:-])
            print(episode)
            print(id_anime)
            with self.open_db_connection() as mycursor:
                response                =   {}
                # get episode
                mycursor.execute("SELECT * FROM episodes WHERE id_anime = %s AND episode = %s",[id_anime,episode])
                response['episode']     =   mycursor.fetchone()
                response['episode']['links'] = [{'server':i+1,'link':link} for i,link in enumerate(response['episode']['links'].split('|'))]
                try:
                    response['episode']['episodeDisplay'] = int(response['episode']['episode'])
                except:
                    response['episode']['episodeDisplay'] = response['episode']['episode']
                current_index           =   response['episode']['index_ep']
                # get anime url
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
        