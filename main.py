import recommendations
import db
import time

def run():
  database = db.connect()
  cursor = db.getCursor(database)

  t1 = time.time()
  results = recommendations.getRecommendations(cursor, 3)
  t2 = time.time()
  prettyPrint(cursor, 3, results)
  t3 = time.time()
  print "REQUIRED TIME FOR RECOMENDATIONS: %0.3f ms, for querying and printing: %0.3f ms" % ((t2-t1)*1000.0, (t3-t2)*1000.0)
  results = recommendations.getRecommendations(cursor, 4)
  prettyPrint(cursor, 4, results)
  db.disconnect(cursor)

def prettyPrint(cursor, uid, results):
  username = db.getUsername(cursor, uid)
  print str(username) + "'s top matches:"
  for result in results:
    wine_name = db.getWineInfoString(cursor, result[1])
    print "%0.3f: %s" % (result[0], wine_name)
