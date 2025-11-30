from app.views.login import LoginScreen
from app.db.database_connection import Database

Database.setUp()
app = LoginScreen()
app.mainloop()
Database.tearDown()
