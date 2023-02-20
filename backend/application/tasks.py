from application.clry import celery
from jinja2 import Template
from weasyprint import HTML
import csv
import os
from application.emailgen import send_email
from application.models import User, List, Card

def format_report(template1,data,User="User"):
    with open(template1) as file:
        temp = Template(file.read())
        return temp.render(data=data,User=User)


def pdf_report(d,User):
    msg = format_report("MAD2_New/backend/templates/monthly_report.html",data=d,User=User)
    html = HTML(string=msg)
    file_name = str(User)+"_Kanban"+".pdf"
    print(file_name)
    html.write_pdf(target=file_name)

wrkng_dir = os.path.abspath(os.path.dirname(__file__))
path_s = os.path.join(wrkng_dir, "static/")
path_t = os.path.join(wrkng_dir, "templates/")

@celery.task()
def export_list(d, username, email):
    with open(path_s+'lists_info_'+username+'.csv', 'w', encoding='utf8', newline='') as f:
        file = csv.DictWriter(f,fieldnames=d[0].keys(),restval='')
        file.writeheader()
        file.writerows(d)
    
    with open(path_t+'list_csv.html','r') as f:
        template = Template(f.read())
    send_email(to_address=email,subject='Exported List Details',message=template.render(user=username,data=d),content="html",attachment=path_s+'lists_info_'+username+'.csv')    
    return "Csv created."

@celery.task()   
def export_card(d, i, username, email, lname):
    with open(path_s+'cards_info_'+str(i)+'.csv', 'w', encoding='utf8', newline='') as f:
        file = csv.DictWriter(f,fieldnames=d[0].keys(),restval='')
        file.writeheader()
        file.writerows(d)
    with open(path_t+'cards_csv.html','r') as f:
        template = Template(f.read())
    send_email(to_address=email,subject='Exported Card Details',message=template.render(user=username,data=d, Name=lname),content="html",attachment=path_s+'cards_info_'+str(i)+'.csv')
    return "Csv created."

@celery.task()
def daily_reminder():
    user_details =User.query.all()
   
    for u in user_details :
        email = u.email
        usr = User.query.filter_by(email = u.email).first()
        username = usr.username
        
        lsts=usr.lists
        list_ids=[]
        for i in lsts:
            list_ids.append(i.list_id)
        cd=[]
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
            for k in details:
                if(k.completion_date==None):                
                    card_dict = {"card_id":k.card_id ,"card_content":k.card_content,"card_name":k.card_name,"deadline_date": str(k.deadline_date)}
                    cd.append(card_dict)
        with open(path_t+'daily_reminder.html','r') as f:
            template = Template(f.read())
        send_email(email,'Daily Reminder',template.render(user=username, cards=cd),content="html")

@celery.task()
def monthly_reminder():
    user_details =User.query.all()
    user_email_list =[]
    data =[]
    u_list =[]
    
    for u in user_details :
        user_email_list.append(u.email)
        user = User.query.filter_by(email = u.email).first()
        username = user.username
        u_list.append(username)
        lists  = user.lists
        list_ids = []
        for i in lists:
            list_ids.append(i.list_id)
        details = []
        count=0
        t=[]
        for j in list_ids:
            count+=1    
            l = List.query.filter_by(list_id=j).first()
            list_name = l.list_name
            list_description = l.list_description
            l_timestamp = l.l_timestamp
            cards  = l.cards
            cmp=0
            incmp=0
            pasd=0
            tot=0
            for i in cards:
                tot+=1
                if(i.completion_date):
                    if(i.completion_date<=i.deadline_date):
                        cmp+=1
                    else:
                        pasd+=1
                else:
                    incmp+=1
            track_dict = {"SNo":count ,"List_Name":list_name,"List_Description":list_description, "date_created": l_timestamp, "completed":cmp, "incomplete": incmp, "passed_dead": pasd}
            t.append(track_dict)
        pdf_report(t,username)

        with open(path_t+'monthly_report.html','r') as f:
            template = Template(f.read())
        send_email(u.email,'Monthly Report',template.render(User=username,data=t),content="html",attachment="./"+str(username)+"_Kanban.pdf")    
    data.append(t)

