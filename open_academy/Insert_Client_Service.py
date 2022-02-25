import functools
import xmlrpclib
HOST = 'localhost'
PORT = 8069
DB = 'Odoo15'
USER = 'odoo'
PASS = 'adminodoo'
ROOT = 'http://%s:%d/xmlrpc/' % (HOST,PORT)

# 1. Login
uid = xmlrpclib.ServerProxy(ROOT + 'common').login(DB,USER,PASS)
print ("Logged in as %s (uid:%d)" % (USER,uid))

call = functools.partial(
    xmlrpclib.ServerProxy(ROOT + 'object').execute,
    DB, uid, PASS)

# 2. Read the sessions
sessions = call('open_academy.sesion','search_read', [], ['title','seats'])
for session in sessions:
    print ("Session %s (%s seats)" % (session['title'], session['seats']))


# 3.create a new session for the "Functional" course
course_id = call('open_academy.course', 'search', [('title','ilike','Functional')])[0]
session_id = call('open_academy.sesion', 'create', {
    'title' : 'My session',
    'id_course' : course_id,
})