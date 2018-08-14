from mydb import MyDB
import pytest

# setting scope = module will allow the setup to only occur once-- hence why we only see print setting up once
@pytest.fixture(scope="module")
# what we really need here is a cursor
def cur():
	print("setting up dB")
	# create the database object--this will give me DB object
	db = MyDB()
	# you always need to connect your DB to a server -- this would normally be acutal server
	conn = db.connect("server")
	# next we will get a cursor object
	curs = conn.cursor()

	# it will create the cursor object only once, and then it will pass the cursor object to test cases
	# after this is complete, it will close the cursor and connection
	yield curs

	curs.close()
	conn.close()
	print("closing dB")

# now all we need to do is pass cur into our two test methods
# pytest fixture will realise there is a cursor function which is a fixture 
# so it will call that function and return the cur object

def test_johns_id(cur):
	# this will return to me the employee ID of the emp. object whose name is john
	id = cur.execute("select id from employee_db where name=John")
	assert id == 123


def test_toms_id(cur):
	# this will return to me the employee ID of the emp. object whose name is john
	id = cur.execute("select id from employee_db where name=Tom")

	assert id == 789


# what is the problem with this approach?
# you are repeating all of these lines of code -- db, conn, curr
# second thing, database connection is costly-- you also may be running tests that require network connection which is costly
# in classic unit test style you will use setup and teardown methods
# this will initialize what you need for your test cases in the beggining