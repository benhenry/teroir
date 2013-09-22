import MySQLdb

def connect():
  db = MySQLdb.connect(host="localhost", user="ferment", passwd="grapes!", db="ferment")
  return db

def getCursor(database):
  # create a cursor
  cursor = database.cursor()
  return cursor

def disconnect(cursor):
  cursor.close()

def getUsersPreferences(cursor, uid):
  cursor.execute("""SELECT wines_id, rating FROM ratings WHERE users_id=%s""", (uid,))
  result = cursor.fetchall()
  return result

def userRatedItem(cursor, uid, wine_id):
  cursor.execute("""SELECT id FROM ratings WHERE users_id=%s AND wines_id=%s""", (uid, wine_id,))
  result = cursor.fetchall()
  # test if true or not
  return result

def getRating(cursor, uid, wine_id):
  cursor.execute("""SELECT rating FROM ratings WHERE users_id=%s AND wines_id=%s""", (uid, wine_id,))
  results = cursor.fetchone()
  return results[0]

def getUniqueUid(cursor):
  cursor.execute("""SELECT DISTINCT id FROM users""")
  results = cursor.fetchall()
  return results

def getUsername(cursor, uid):
  cursor.execute("""SELECT username FROM users WHERE id=%s""", (uid,))
  results = cursor.fetchone()

def getUniqueRatedWines(cursor):
  cursor.execute("""SELECT DISTINCT wines_id FROM ratings""")
  results = cursor.fetchall()
  return results

def getAverageRating(cursor, wine_id):
  cursor.execute("""SELECT AVG(rating) FROM ratings WHERE wine_id=%s""", (wine_id,))
  results = cursor.fetchone()
  return results[0]

def getHighestRatedWines(cursor, n=10):
  cursor.execute("""SELECT a.wines_id, a.average FROM
                    (
                      SELECT rate.wines_id, AVG(rating) AS average
                      FROM ratings rate
                      RIGHT OUTER JOIN
                      (
                        SELECT DISTINCT wines_id
                        FROM ratings
                      ) AS r
                      ON rate.wines_id=r.wines_id
                      GROUP BY wines_id
                    ) AS a
                    ORDER BY a.average
                    DESC LIMIT %s;""", (n,))
  results = cursor.fetchall()
  return results

def getWineInfoString(cursor, wine_id):
  vintage = getVintage(cursor, wine_id)
  type = getWineType(cursor, wine_id)
  producer = getWineProducer(cursor, wine_id)
  variety = getWineVariety(cursor, wine_id)
  designation = getWineDesignation(cursor, wine_id)
  vineyard = getVineyard(cursor, wine_id)
  country = getCountryOfOrigin(cursor, wine_id)
  region = getRegion(cursor, wine_id)
  subregion = getSubRegion(cursor, wine_id)
  appellation = getAppellation(cursor, wine_id)
  return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (vintage, type, producer, variety, designation, vineyard, country, region, subregion, appellation)

def getVintage(cursor, wid):
  cursor.execute("""SELECT vintage FROM wine_list WHERE id=%s""", (wid,))
  result = cursor.fetchone()
  return "NV" if result[0] == 0 else str(result[0])

def getWineType(cursor, wid):
  cursor.execute("""SELECT value FROM wine_types WHERE id=(SELECT type FROM wine_list WHERE id=%s)""", (wid,))
  result = cursor.fetchone()
  return str(result[0])

def getWineProducer(cursor, wid):
  cursor.execute("""SELECT value FROM wine_producers WHERE id=(SELECT producer FROM wine_list WHERE id=%s)""", (wid,))
  result = cursor.fetchone()
  return str(result[0])

def getWineVariety(cursor, wid):
  cursor.execute("""SELECT value FROM wine_varieties WHERE id=(SELECT variety FROM wine_list WHERE id=%s)""", (wid,))
  result = cursor.fetchone()
  return str(result[0])

def getWineDesignation(cursor, wid):
  cursor.execute("""SELECT value FROM wine_designations WHERE id=(SELECT designation FROM wine_list WHERE id=%s)""", (wid,))
  result = cursor.fetchone()
  return str(result[0])

def getVineyard(cursor, wid):
  cursor.execute("""SELECT value FROM wine_vineyards WHERE id=(SELECT vineyard FROM wine_list WHERE id=%s)""", (wid,))
  result = cursor.fetchone()
  return str(result[0])

def getCountryOfOrigin(cursor, wid):
  cursor.execute("""SELECT value FROM wine_countries WHERE id=(SELECT country FROM wine_list WHERE id=%s)""", (wid,))
  result = cursor.fetchone()
  return str(result[0])

def getRegion(cursor, wid):
  cursor.execute("""SELECT value FROM wine_regions WHERE id=(SELECT region FROM wine_list WHERE id=%s)""", (wid,))
  result = cursor.fetchone()
  return str(result[0])

def getSubRegion(cursor, wid):
  cursor.execute("""SELECT value FROM wine_subregions WHERE id=(SELECT subregion FROM wine_list WHERE id=%s)""", (wid,))
  result = cursor.fetchone()
  return str(result[0])

def getAppellation(cursor, wid):
  cursor.execute("""SELECT value FROM wine_appellations WHERE id=(SELECT appellation FROM wine_list WHERE id=%s)""", (wid,))
  result = cursor.fetchone()
  return str(result[0])


