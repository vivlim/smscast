import config
import MySQLdb

PHONE_NUM_COL = 2

class LibAddrBook:
	def __init__(self):
		self.db = MySQLdb.connect(user=config.MYSQL_USER, passwd=config.MYSQL_PASSWD, db=config.MYSQL_DB)
	def get_everyone(self):
		c = self.db.cursor()
		c.execute("""SELECT * from people""")
		nums = []
		for row in c.fetchall():
			print(row)
			nums.append(row[PHONE_NUM_COL])

		return nums
