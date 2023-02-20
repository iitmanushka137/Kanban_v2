from flask import Flask
from flask_security import SQLAlchemyUserDatastore, Security,hash_password
from flask_cors import CORS
from application.models import db, User, Role
from application.api import UserAPI, ListAPI, CardAPI, SummaryAPI, ExportCards, ExportList
from flask_restful import Api
import os
from celery.schedules import crontab
import application.clry as clry
from application.cache import cache
from application.tasks import daily_reminder, monthly_reminder

app = Flask(__name__)
app.secret_key = "thisisasecertkey"
app.config['WTF_CSRF_ENABLED'] = False
current_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+os.path.join(current_dir, "project.sqlite3")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECURITY_PASSWORD_SALT'] = 'thisisasecretsalt'
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = 'Authentication-Token'
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/1'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/2'
app.config['CELERY_ENABLE_UTC'] = False
app.config['CELERY_TIMEZONE']='Asia/Kolkata'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/3'
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 100

api=Api(app)
CORS(app)
db.init_app(app)
cache.init_app(app)

api.add_resource(UserAPI,"/api/user","/api/user/<string:email>")
api.add_resource(ListAPI, "/api/list/<string:email>", "/api/list/<string:email>/<int:lid>")
api.add_resource(CardAPI, "/api/card/<string:email>", "/api/card/<string:email>/<int:lid>", "/api/card/<string:email>/<int:olid>/<int:cid>")
api.add_resource(SummaryAPI, "/api/summary/<string:email>")
api.add_resource(ExportList, "/api/exportList/<string:email>")
api.add_resource(ExportCards, "/api/exportCard/<string:email>/<int:lid>")

celery = clry.celery
app.app_context().push()

celery.conf.update(
     broker_url='redis://localhost:6379/1',
     result_backend='redis://localhost:6379/2'
 )

celery.Task = clry.ContextTask
app.app_context().push()


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

@app.before_first_request
def create_tables():
    db.create_all()

@app.before_first_request
def create_user():
    if not user_datastore.find_user(email="krishnaanushka137@gmail.com"):
        user_datastore.create_user(email="krishnaanushka137@gmail.com",username="Anushka",password=hash_password("password"))
    db.session.commit()  

@app.route('/')
def hello():
    return 'hello'

# delta_d=d.timedelta(minutes=5.0)
# delta_m=d.timedelta(minutes=3.0)

# celery.conf.beat_schedule = {
# # 'task-daily': {
# #     'task': 'application.tasks.daily_reminder',
# #     'schedule': schedule(delta_d),
# # },
# 'task-monthly': {
#     'task': 'application.tasks.monthly_reminder',
#     'schedule': schedule(delta_m),
# },
# }

import datetime
import pytz
def timee(): 
    return datetime.datetime.now(pytz.timezone('Asia/Kolkata')) 


@celery.on_after_finalize.connect
def monthly_report(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=9, minute=30, day_of_month="1", nowfun=timee),
        monthly_reminder.s(),
    )
    sender.add_periodic_task(
        crontab(hour=9, minute=30, day_of_week='*', nowfun=timee),
        daily_reminder.s(),
    )


celery.conf.timezone = 'Asia/Kolkata'

if __name__=='__main__':
    app.run(debug=True)

#redis-server in redis at desktop
#npm run serve in frntend
#python3 app.py in bkend
#mailhog
#celery -A app.celery beat --max-interval 1 -l info in bkend
#celery -A app.celery worker -l info in bkend
