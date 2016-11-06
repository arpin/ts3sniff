from collections import namedtuple
import dateutil.parser
import re
import datetime
import csv

Ts3LogRow = namedtuple('Ts3LogRow', ['dt','level','cls','msg','event','user','userid'])

class Event(object):
	def __init__(self, name='unknown', rx=None, rxuser=re.compile(r"'(.+?)'"), rxuserid=re.compile(r"\(id:(.+?)\)")):
		self.name = name
		self.rx = rx
		self.rxuser = rxuser
		self.rxuserid = rxuserid
	def test(self, msg):
		if self.rx is None:
			return None
		return self.rx.match(msg)
	def user(self,msg):
		m = self.rxuser.search(msg)
		return m.group(1) if m else None
	def userid(self,msg):
		m = self.rxuserid.search(msg)
		return m.group(1) if m else None
	def __repr__(self):
		return 'Event:'+self.name

events = [
	Event('connected', re.compile(r"^client connected.*")),
	Event('disconnected', re.compile(r"^client disconnected.*")),
]

def process_event(msg):
	for e in events:
		if e.test(msg):
			return e
	return Event()

def secs2human(secs):
	return str(datetime.timedelta(seconds=secs))
def datetime2unixtimestamp(dt):
	return int((dt - datetime.datetime(1970,1,1)).total_seconds())

class Connections(object):
	def __init__(self):
		self.usernames = {}
		self.connections = {}
	def chew(self,log):
		# fill username by userid
		for x in log:
			if x.event.name == 'connected':
				if x.userid not in self.usernames:
					self.usernames[x.userid] = set([x.user])
				else:
					self.usernames[x.userid].add(x.user)
		# get times connected for each userid
		for x in log:
			if x.event.name == 'connected' or x.event.name == 'disconnected':
				if x.userid not in self.connections:
					self.connections[x.userid] = [[None,None,0]]
				# the last conn/disconn pair is already filled, create a new
				if self.connections[x.userid][-1][1] is not None:
					self.connections[x.userid].append([None,None,0])
				# fill the last conn/disconn pair
				if x.event.name == 'connected':
					self.connections[x.userid][-1][0] = x
				elif x.event.name == 'disconnected':
					self.connections[x.userid][-1][1] = x
					a = self.connections[x.userid][-1][0]
					b = self.connections[x.userid][-1][1]
					self.connections[x.userid][-1][2] = (b.dt-a.dt).total_seconds() if a is not None and b is not None else 0
	def userid2name(self,userid):
		return ", ".join(self.usernames[userid])
	def overview(self):
		a = [(k,sum([x[2] for x in v]),len(v)) for k,v in self.connections.iteritems()]
		return sorted(a, key=lambda x: x[1], reverse=True)
	def stats(self):
		a = [
			(
				k,
				self.userid2name(k),
				datetime2unixtimestamp(x[0].dt) if x[0] else None,
				datetime2unixtimestamp(x[1].dt) if x[1] else None,
				x[2]
			)
			for k,v in self.connections.iteritems()
			for x in v
		]
		return sorted(a, key=lambda x: x[2])
	def csvdump(self):
		with open('stats.csv', 'wb') as f:
			w = csv.writer(f)
			w.writerow(['userid','name','connected','disconnected','online'])
			for row in self.stats():
				w.writerow(row)
	def printoverview(self):
		print "{:40} {:30} {:10}".format("Name", "Time online", "Times connected")
		for x in self.overview():
			print "{:40} {:30} {:10}".format(self.userid2name(x[0]), secs2human(x[1]), x[2])
	def test(self):
		for k,v in self.connections.iteritems():
			print self.userid2name(k) + ": "
			for x in v:
				print "  " + str(x[0].dt if x[0] else None) + " => " + str(x[1].dt if x[1] else None) + " | " +  secs2human(x[2])

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('logfile')
	parser.add_argument('-w', '--weeks', type=int, default=0)
	args = parser.parse_args()

	log = []
	with open(args.logfile, "r") as f:
		for line in f:
			x = map(lambda x: x.strip(), line.split('|'))
			dt=dateutil.parser.parse(x[0])
			if args.weeks > 0:
				if dt < datetime.datetime.now()-datetime.timedelta(weeks=args.weeks):
					continue
			msg = x[4]
			e = process_event(msg)
			log.append(Ts3LogRow(
				dt=dt,
				level=x[1],
				cls=x[2],
				msg=msg,
				event=e,
				user=e.user(msg),
				userid=e.userid(msg),
			))

	print "Log from " + str(log[0].dt) + " to " + str(log[-1].dt)
			
	c = Connections()
	c.chew(log)	
	#c.printoverview()
	c.csvdump()
