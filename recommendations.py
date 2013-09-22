from math import sqrt
import db

# Returns a distance-based similarity score for person1 and person2
def sim_distance(cursor, uid1, uid2):
  # Get the list of shared_items
  si={}
  sum_of_squares = 0
  # Query DB for uid1's prefs and then iterate through them.
  for item in db.getUsersPreferences(cursor, uid1):
    # Query DB for uid2's prefs and then iterate through them.
    if db.userRatedItem(cursor, uid2, item[0]):
      item2 = db.getRating(cursor, uid2, item[0])
      si[item]=1
      sum_of_squares += pow(item[1] - item2, 2)

  # If they have no ratings in common, return 0
  if len(si) == 0: return 0

  # Add up the squares of all the differences
  # Either store the rec score of each matching item, or run a bunch of queries here.

  print "Compared to user " + str(uid2) + ", likeness is " + str(1 / (1+sqrt(sum_of_squares)))

  return 1/(1+sqrt(sum_of_squares))

# Returns the Pearson correlation coefficient for p1 and p2
def sim_pearson(cursor, uid1, uid2):
  # Get the list of mutually rated items
  sum1 = 0
  sum2 = 0
  sum1Sq = 0
  sum2Sq = 0
  pSum = 0
  n = 0

  for item in db.getUsersPreferences(cursor, uid1):
    if db.userRatedItem(cursor, uid2, item[0]):
      item2 = db.getRating(cursor, uid2, item[0])
      sum1 += item[1]
      sum1Sq += pow(item[1], 2)
      sum2 += item2
      sum2Sq += pow(item2, 2)
      pSum += (item[1]*item2)
      n += 1

  # if there are no ratings in common, return 0
  if n == 0: return 0

  # Add up all the preferences

  # Sum up the squares

  # Sum up the products

  # Calculate Pearson score
  num = pSum-(sum1*sum2/n)
  den = sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))

  if den==0: return 0

  r = num/den

  return r

# Returns the best matches for person from the prefs dictionary.
# Number of results and similarity function are optional params.
def topMatches(cursor, uid, n=5, similarity=sim_pearson):
  # Get list of unique IDs, and iterate through those.  Make sure the don't match the person input
  results = db.getUniqueUid(cursor)
  print "RESULTS FOR USER " + str(uid)
  scores=[(similarity(cursor, uid, other[0]), other[0]) for other in results if other[0] != uid]

  # Sort the list so the hightest scores appear at the top
  scores.sort()
  scores.reverse()
  return scores[0:n]

# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def getRecommendations(cursor, person, similarity=sim_pearson):
  # IF WE NEED TO OPTIMIZE THIS ALGORITHM:
  # We should run topMatches for each user in a cron job and keep the top 5-10 matches of users
  # Then, we can run the second half of this algorithm at login time to find top matched wines.
  # A second optimization could be to filter out the top rated wines and only compare those wines rather than all wines
  totals={}
  simSums={}
  results = db.getUniqueUid(cursor)
  for result in results:
    # don't compare me to myself
    if result[0]==person: continue
    sim = similarity(cursor, person, result[0])

    # ignore scores of zero or lower
    if sim <= 0: continue
    for item in db.getUsersPreferences(cursor, result[0]):
      # only score prefs not in my list
      if db.userRatedItem(cursor, person, item[0]) != 0 or item[1] == 0:
        other_rating = db.getRating(cursor, result[0], item[0])
        # Similarity * Score
        totals.setdefault(item[0], 0)
        totals[item[0]] += other_rating*sim
        # Sum of similarities
        simSums.setdefault(item[0], 0)
        simSums[item[0]] += sim

  # Create the normalized list
  rankings = [(total / simSums[item], item) for item,total in totals.items() if total / simSums[item] > 80]

  # Return the sorted list
  rankings.sort()
  rankings.reverse()
  return rankings

# Haven't worked on this yet.  Please validate work in getRecommendations and topMatches first
#def transformPrefs(prefs):
#  result={}
#  for person in prefs:
#    for item in prefs[person]:
#      result.setdefault(item,{})
#
#      # Flip item and person
#      result[item][person]=prefs[person][items]
#  return result

# Find the top n wines as rated by the community.  Allow user to specify a range of dates to get the highest rated wines from a period.
def highestRatedWines(cursor, n=10, since=0, until=0):
  # TODO: Add in date cutoffs.
  return db.getHighestRatedWines(cursor, n)


