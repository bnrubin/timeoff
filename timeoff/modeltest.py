from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
import models
from datetime import datetime

engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(engine)

session = Session()

models.Base.metadata.create_all(engine)

manager = models.Employee(name_last='Supervisor', name_first='Mark')

me = models.Employee(name_last='Rubin', name_first='Benjamin', email='bnrubin@nullcortex.com', manager=manager)
jas = models.Employee(name_last='Doe', name_first='Jane', email='jdoe@example.com', manager=manager)
session.add(manager)
session.commit()
session.add_all((me,jas))
session.commit()

req = models.Request(start_date=datetime.now(), end_date=datetime.now(),employee_id=me.id)

session.add(req)
session.commit()

print(me.requests_pending)
