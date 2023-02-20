from flask_restful import Resource, reqparse, fields, marshal_with
from application.models import db, User as user_model, Role, List, Card, Completed, CompletedStats
import datetime as d
from flask_security import auth_required, current_user, hash_password, SQLAlchemyUserDatastore, Security, login_required
from flask import jsonify
import matplotlib.pyplot as plt
import os
import application.tasks as tasks
from application.cache import cache

wrkng_dir = os.path.abspath(os.path.dirname(__file__))

user_datastore = SQLAlchemyUserDatastore(db, user_model, Role)
security = Security(user_datastore)

figure = plt.figure()

user_req_args = reqparse.RequestParser()
user_req_args.add_argument('username',required=True,help="username required")
user_req_args.add_argument('email',required=True,help="email required")
user_req_args.add_argument('password',required=True,help="password required")

user_fields = {
    'username' : fields.String ,
    'email' : fields.String ,
}

class UserAPI(Resource):
    @auth_required('token')
    @marshal_with(user_fields)
    def get(self):
        return current_user

    @marshal_with(user_fields)
    def post(self):
        args = user_req_args.parse_args()
        
        email = args.get("email")
        user_name = args.get("username")
        passw = args.get("password")
        check=user_model.query.filter_by(email=email).first()
        if check:
           return jsonify('email you entered already belongs to an account. Try another email.')
        else:    
            user_datastore.create_user(email=email,username=user_name,password=hash_password(passw))
            db.session.commit()
            data = user_model.query.filter_by(email=email).first()
            return data

list_req_args=reqparse.RequestParser()
list_req_args.add_argument('list_name', required=True, help="list name is required")
list_req_args.add_argument('list_description')
list_req_args.add_argument('email',required=True,help="email required")
list_req_args.add_argument('lid')

list_fields={
    "email" : fields.String,
    'list_name': fields.String,
    'list_description': fields.String
}

class ListAPI(Resource):
    @auth_required('token')
    def get(self, email):
        try:
            u=user_model.query.filter_by(email=email).first()
            l=u.lists
            list_ids=[]
            for i in l:
                list_ids.append(i.list_id)
            ls=[]
            for j in list_ids:
                ap=List.query.filter_by(list_id=j).first()
                ls.append(ap)

            cnt = 0  
            d = {}  
            for k in ls:
                cnt+=1
                list_dict = {"list_id":k.list_id ,"list_name":k.list_name,"list_description":k.list_description, "l_timestamp": str(k.l_timestamp) }
                d[cnt]=list_dict

            return jsonify(d)
        except:
            return jsonify({"error": "Wrong details fed and asked for."})

    @auth_required('token')
    def post(self, email):
        agrs=list_req_args.parse_args()

        eid=email
        lname=agrs.get("list_name")
        ldes = agrs.get("list_description", None)

        n_list=List(list_name=lname, list_description=ldes, l_timestamp=d.date.today())
        u=user_model.query.filter_by(email=eid).first()
        u.lists.append(n_list)
        db.session.add(n_list)
        db.session.commit()

        mg="List Created"
        return jsonify(mg)

    @auth_required('token')
    def put(self, lid, email):
        l=List.query.filter_by(list_id=lid).first()
        args=list_req_args.parse_args()

        eid=email

        lname=args.get('list_name')
        ldes=args.get('list_description', None)

        if l:
            l.list_name=lname
            l.list_description=ldes
            db.session.commit()
            return jsonify("List Updated")

        return jsonify({"error": "Invalid list id"})

    @auth_required('token')
    def delete(self, lid, email):
        eid=email
        l_t_d=List.query.filter_by(list_id=lid).first()
        cds=l_t_d.cards
        card_ids=[]
        for i in cds:
            card_ids.append(i.card_id)
        try:
            for j in card_ids:
                Card.query.filter_by(card_id = j).delete()
                db.session.commit()
            db.session.delete(l_t_d)
            db.session.commit()
            return jsonify("Deleted Successfully")
        except:
            return jsonify({"error": "Invalid list id"})

card_post_args = reqparse.RequestParser()
card_post_args.add_argument('card_name',required=True,help="card name required")
card_post_args.add_argument('card_content',required=True,help="card content required")
card_post_args.add_argument('deadline_date',required=True,help="deadline date required")
card_post_args.add_argument('completion_date')
card_post_args.add_argument('email',required=True,help="email required")
card_post_args.add_argument('lid')
card_post_args.add_argument('cid')

card_fields={
    "email": fields.String,
    "card_name": fields.String,
    "card_content": fields.String,
    "deadline_date": fields.String,
    "dompletion_date": fields.String
}

class CardAPI(Resource):
    @auth_required('token')
    @cache.memoize(50)
    def get(self, email):
        try:
            u=user_model.query.filter_by(email=email).first()
            ur = {'username':u.username}
            l=u.lists
            list_ids=[]
            for i in l:
                list_ids.append(i.list_id)
            ls=[]
            for j in list_ids:
                ap=List.query.filter_by(list_id=j).first()
                ls.append(ap)

            cnt = 0  
            lt = {}  
            for k in ls:
                cnt+=1
                list_dict = {"list_id":k.list_id ,"list_name":k.list_name,"list_description":k.list_description, "l_timestamp": str(k.l_timestamp) }
                lt[cnt]=list_dict
            cd={}
            for i in list_ids:
                parent_list=List.query.filter_by(list_id=i).first()
                all_cards = parent_list.cards 
                card_ids = []
                for j in all_cards:
                    card_ids.append(j.card_id)
                details = []    
                for j in card_ids:    
                    detail = Card.query.filter_by(card_id=j).first()
                    details.append(detail)
                nd={}
                for k in details:
                    card_dict = {"card_id":k.card_id ,"card_content":k.card_content,"card_name":k.card_name,"deadline_date": str(k.deadline_date),"created_date": str(k.created_date), "completed_date": str(k.completion_date)}
                    nd[k.card_id]=card_dict
                cd[i]=nd
            return jsonify(ur, lt, cd)
        
        except:
            return jsonify({"error": "Wrong details fed and asked for."})

    @auth_required('token')
    def post(self, email, lid):
        agrs = card_post_args.parse_args()
        eid=email
        u=user_model.query.filter_by(email=eid).first()
        cname=agrs.get("card_name")
        ccont = agrs.get("card_content")
        dd=agrs.get("deadline_date")
        c_d = d.date(int(dd[:4]), int(dd[5:7]), int(dd[-2:]))
        cd=agrs.get("completion_date", None)
        lid=agrs.get("lid")
        parent_list=List.query.filter_by(list_id=lid).first()
        comp_dt=None
        if cd:
            comp_dt=d.date.today()

        n_cd=Card(card_name=cname, card_content=ccont, deadline_date=c_d, completion_date=comp_dt, created_date=d.date.today(), last_updated=d.date.today())
        parent_list.cards.append(n_cd)
        db.session.add(n_cd)
        db.session.commit()

        return jsonify("Card Created")

    @auth_required('token')
    def put(self, email, olid, cid):
        agrs = card_post_args.parse_args()
        eid=email
        cname=agrs.get("card_name")
        ccont=agrs.get("card_content")
        dd=agrs.get("deadline_date")
        c_d = d.date(int(dd[:4]), int(dd[5:7]), int(dd[-2:]))
        cc=agrs.get("completion_date")
        comp_dt=None
        if cc:
            comp_dt=d.date.today()
        c = Card.query.filter_by(card_id=cid).first()
        if c:
            c.card_name=cname
            c.card_content=ccont
            c.deadline_date = c_d
            c.completion_date=comp_dt
            c.last_updated=d.date.today()
            c.list_id=olid
            db.session.commit()
            return jsonify("Card Updated")
        return jsonify({"error": "Card can't be updated"})

    @auth_required('token')
    def delete(self, email, lid):
        c_t_d=Card.query.filter_by(card_id=lid).first()
        eid=email
        try:
            db.session.delete(c_t_d)
            db.session.commit()
            return jsonify("Deleted Successfully")
        except:
            return jsonify({"error": "Invalid card id"})

import base64
class SummaryAPI(Resource):

    @auth_required('token')
    @cache.memoize(timeout=50)
    def get(self, email):
        try:
            u=user_model.query.filter_by(email=email).first()
            ur = {'user_name': u.username}
            l = u.lists
            list_ids=[]
            for i in l:
                list_ids.append(i.list_id)
            Completed.query.delete()
            db.session.commit()
            CompletedStats.query.delete()
            db.session.commit()
            lt={}
            stat={}
            for j in list_ids:
                dt = List.query.filter_by(list_id=j).first()
                list_details = {'list_id':dt.list_id, 'list_name':dt.list_name}
                lt[dt.list_id]=list_details

                cds=dt.cards
                card_ids = []
                for i_ in cds:
                    card_ids.append(i_.card_id)
                total = len(card_ids)
                comp=0
                pass_dead = 0
                incomp=0
                for j_ in card_ids:
                    cd = Card.query.filter_by(card_id=j_).first()
                    if(cd.completion_date):
                        if(cd.completion_date<=cd.deadline_date):
                            chk = Completed.query.filter_by(list_id=j).filter_by(completion_date=cd.completion_date).first()
                            if(chk):
                                chk.count+=1
                                db.session.commit()
                            else:
                                n_ent = Completed(list_id=j, completion_date=cd.completion_date, count=1)
                                db.session.add(n_ent)
                                db.session.commit()
                            comp+=1
                        else:
                            pass_dead+=1
                    else:
                        incomp+=1
                st_ent = CompletedStats(list_id=j, total_cards=total, completed_cards=comp, passed_deadline=pass_dead, incomplete_cards=incomp)
                db.session.add(st_ent)
                db.session.commit()
            
            for _l in list_ids:
                fnd = CompletedStats.query.filter_by(list_id=_l).first()
                dt={'list_id':fnd.list_id, 'total_cards':fnd.total_cards, 'completed_cards':fnd.completed_cards, 'incomplete_cards':fnd.incomplete_cards, 'passed_deadline':fnd.passed_deadline}
                stat[_l]=dt

            for r in list_ids:
                ccd = db.session.query(Completed).filter_by(list_id = r).all()
                plt.clf()
                # axes = figure.add_subplot(1,1,1)
                # axes.plot([str(d.completion_date) for d in ccd],
                #     [e.count for e in ccd])
                # plt.xticks(rotation = 45)
                x_l = [str(d.completion_date) for d in ccd]
                y_l = [e.count for e in ccd]
                plt.plot(x_l, y_l, c='r', ls='dashed', marker='o')
                path = os.path.join(wrkng_dir, "static/IMG/")
                # figure.savefig(path+str(r)+".png")
                plt.savefig(path+str(r)+".png")

            
            imgs = {}
            for r in list_ids:
                encoded = base64.b64encode(open(path+str(r)+".png", "rb").read())
                new_encode = str(encoded)[2:-3]
                imgs[r]=str(new_encode)
            return jsonify(ur, lt, stat, imgs)

        except:    
            return jsonify({"error" :"There are some wrong user details filled and asked for."})

class ExportList(Resource):
    @auth_required('token')
    def get(self,email):
        try:
            user = user_model.query.filter_by(email = email).first()
            username = user.username
            uid = user.id
            lists  = user.lists
            if(lists):
                list_ids = []
                for i in lists:
                    list_ids.append(i.list_id)
                details = []    
                for j in list_ids:    
                    detail = List.query.filter_by(list_id=j).first()
                    details.append(detail)
                cnt = 0  
                l = []
                for k in details:
                    cnt+=1
                    list_dict = {"SNo":cnt ,"List_Name":k.list_name,"List_Description":k.list_description, "Date_Created": str(k.l_timestamp)}
                    l.append(list_dict)

                List_exp = tasks.export_list.delay(l, username, email)
                return jsonify("Lists Exported")
            else:
                raise Exception("No lists to export")
            # with open('backend/application/static/lists_info.csv', 'w', encoding='utf8', newline='') as f:
            #     file = csv.DictWriter(f,fieldnames=l[0].keys(),restval='')
            #     file.writeheader()
            #     file.writerows(l)
            
        except:
            return jsonify("Couldn't export")

class ExportCards(Resource):
    @auth_required('token')
    def get(self, email, lid):
        user = user_model.query.filter_by(email = email).first()
        username = user.username
        l=List.query.filter_by(list_id=lid).first()
        cards=l.cards
        card_ids=[]
        for i in cards:
            card_ids.append(i.card_id)
        details=[]
        for j in card_ids:
            detail=Card.query.filter_by(card_id=j).first()
            details.append(detail)
        cnt = 0
        c=[]
        if(details):
            for k in details:
                cnt+=1
                card_dict = {"SNo":cnt, "Card_Name":k.card_name, "Card_Content":k.card_content, "Deadline_Date":k.deadline_date, "Date_Created":k.created_date, "Completed":k.completion_date}
                c.append(card_dict)
        else:
            card_dict = {"SNo":cnt, "Card_Name":None, "Card_Content":None, "Deadline_Date":None, "Date_Created":None, "Completed":None}
            c.append(card_dict)
        Cards_exp = tasks.export_card.delay(c, lid, username, email, l.list_name)

        return jsonify("Cards exported")