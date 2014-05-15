import config
import MySQLdb

PHONE_NUM_COL = 2

class LibAddrBook:
	def __init__(self):
		self.db = MySQLdb.connect(user=config.MYSQL_USER, passwd=config.MYSQL_PASSWD, db=config.MYSQL_DB)
	def get_everyone(self):
		c = self.db.cursor()
		c.execute("""SELECT * from people""")
		ppl = []
		nums = []
		for row in c.fetchall():
			print(row)
			print(row[0])
			nums.append(row[PHONE_NUM_COL])
			ppl.append({'id': row[0], 'name': row[1]})

		return ppl
	def get_groups(self):
		c = self.db.cursor()
		c.execute("""SELECT * from groups""")
		groups = []
		for row in c.fetchall():
			groups.append({'gid': row[0], 'name': row[1]})
		return groups

# todo: make sure ids is actually a list of numbers?
	def get_nums_with_ids(self, ids):
		c = self.db.cursor()
		idlist = ', '.join('{}'.format(x) for x in ids)
		print idlist
		c.execute("""SELECT * from people WHERE id IN ({})""".format(idlist))
		nums = []
		for row in c.fetchall():
			nums.append(row[PHONE_NUM_COL])
		return nums

	def get_people_in_groups(self, groups):
		if(len(groups) == 0):
			return []
		# /!\ SPECIAL CASE ALERT: A group ID of -1 signifies that 'everyone' is selected, so use that function instead.
		if(-1 in groups):
			return [p['id'] for p in self.get_everyone()]

		c = self.db.cursor()
		grouplist = ', '.join('{}'.format(x) for x in groups)
		print grouplist
		c.execute("""SELECT people.id from people INNER JOIN memberships ON people.id = memberships.person_id WHERE memberships.group_id IN ({})""".format(grouplist))
		ids = [r[0] for r in c.fetchall()]
		return ids
