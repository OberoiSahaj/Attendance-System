import sqlite3


#attend.c.execute("select * from attendance")
#print(attend.c.fetchall())

conn = sqlite3.connect('attendance_data.db', check_same_thread=False)

c = conn.cursor()

c.execute("select * from attendance")

print(c.fetchall())
conn.commit()
conn.close()
