# Project - 

Implement an ofiice attendance system which uses mobile no to check in for the users. At the 9pm all the users get checked out
automatically.


## User Level - 

1. Normal User - He can only check in using his mobile no. He can not log out, only way he gets logged out is when session expires.
2. Manager - He has to check in using the login and password. The manager has one more benefit, he can access the attendance sheet
i.e. who is present and when they checked in. Using the normal check in for manager is banned, because people knowing the manager no.
can check the attendance. He can log out any time. 
3. Admin - The extra feature that admin gets with all the functionality of manager is that he can create the user of any level.

# Implementation details - 

The normal sesssion would not work as the details resides at the browser side and to access it User must to be online.
So i opt for Server side session storage. I implemented it using flask-kvsession package.

### Flask-KVSession - 
Session implementation configuration - 
```
import redis
from flask_kvsession import KVSessionExtension
from simplekv.memory.redisstore import RedisStore

st = RedisStore(redis.StrictRedis())

KVSessionExtension(st, app)

```
Whenever you log in, a session key is sent to user and key-value pair is then stored at the server side.
You can access the key using this - 
```
cookie_val = request.cookies.get('session').split(".")[0]
```
and key's value can be checked using this -
```
st.get(cookie_val)
```
Now i can check using the key that whether the session has ended or not. Storing the key in database in the user table so that i can
use it to access the session for any user at any given time.

The settings to make the session persist even after the user have closed the browser-
```
PERMANENT_SESSION_LIFETIME = session_time()
SESSION_PERMANENT = True
```
Don't worry about the session time function, we will see what it does in next paragraph.

The session expires at 9pm and all of them get logged out automatically. To make it possible i have used python datetime library to
make the time calulation that how long the session have to last. The logic is here - 
```
def session_time():
	a = datetime.now()
	y, m, d = [int(i) for i in str(date.today()).split('-')]
	t = datetime(y,m,d,21,0,0,0)
	return t - a
```
a is taking the current time when someone log in and t is the value of datetime of at 9pm on a given date.
The return value here is a timedelta object which is being used for ```PERMANENT_SESSION_LIFETIME```.

### Login Implementation - 
#### For Normal User - 
When user checks in-
```
login_user(user)
cookie_val = request.cookies.get('session').split(".")[0]
user.cookie = cookie_val
user.check_in = str(datetime.now().time())
db.session.add(user)
db.session.commit()
flash('You are checked In, Now.')
```
User gets logged in and a check_in value get stored in the database along with session-id which is coockie_value. A user can't log in
again because route checks to see that if for the user's cookie_value's value exists in session.
```
st.get(user.cookie)
flash('Already logged In')
```
#### For admin and user - 
Since they can login and logout multiple time, the check in time was an important factor to check when they first logged in. To take
care of that -
```
try:
	st.get(user.cookie)
except:
	user.check_in = str(datetime.now().time())
user.cookie = cookie_val
db.session.add(user)
db.session.commit() 
```
Only if the session is expired and they log back in, then the time gets set.

### Attendance and New user - 
#### Manager - 
He can only check the attendance so the implementation is this - 
```
@main.route('/attendance', methods=['GET'])
@is_manager
def attendance():
	users = User.query.all()
	a = []
	for user in users:
		name = user.username
		key = user.cookie
		try:
			value = st.get(key)
		except:
			value = 'Not checked in yet'
			check_in = '----'
		if value != 'Not checked in yet':
			value = 'checked In, Working'
			check_in = user.check_in
		phone_no = user.phone_no

		b = [name, value, check_in[:-10], phone_no ]
		a.append(b)
	return render_template('attendance.html', users=a)
```

To show the attendance, all the users status gets stored in the list and passed to the html template. Only manager or admin can see
this. As admin is manager too.

#### Admin - 
Apart from attendace, admin can create new users too. The implementation is - 
```
@main.route('/new_user', methods=['GET', 'POST'])
@is_admin
def new_user():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, password=form.password.data, phone_no=form.phone_no.data, admin=form.admin.data, manager=form.manager.data)
		db.session.add(user)
		db.session.commit()
		flash('New user has been created')
		return redirect(url_for('.office'))
	return render_template('register.html', form=form)
 ```
 
## Limitation - 
1. I have assumed that no user logs in between 9pm to 12pm.
