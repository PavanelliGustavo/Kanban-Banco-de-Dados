from app.views.app import App
from app.db.database_connection import Database

Database.setUp()
app = App()
app.mainloop()
Database.tearDown()
