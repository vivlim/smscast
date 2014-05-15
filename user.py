import config
import MySQLdb
import hashlib

class User:
	def __init__(self,uid):
		self.uid = uid
		self.db = MySQLdb.connect(user=config.MYSQL_USER, passwd=config.MYSQL_PASSWD, db=config.MYSQL_DB)

		c = self.db.cursor()
		c.execute("""SELECT name FROM users WHERE uid = %s""", (uid,))
		self.name = c.fetchall()[0][0]

	def is_authenticated(self):
		return True # stub

	def is_active(self):
		return True # stub

	def is_anonymous(self):
		return False
	def get_id(self):
		return unicode(self.uid)

		

def get(userid):
	return User(userid)

def authenticate(username, password):
	db = MySQLdb.connect(user=config.MYSQL_USER, passwd=config.MYSQL_PASSWD, db=config.MYSQL_DB)
	c = db.cursor()
	
	# get salt for the user
	c.execute("""SELECT salt, password, uid FROM users WHERE name = %s """ , (username,))
	print "getting salt for {}".format(username)
	if(c.rowcount == 0): return None
	row = c.fetchall()[0]
	salt = row[0]
	userhash = row[1]
	uid = row[2]
	testhash = hashlib.sha1("{}{}".format(password,salt)).hexdigest()
	if testhash == userhash:
		# good
		return uid
	else:
		#bad
		return None

