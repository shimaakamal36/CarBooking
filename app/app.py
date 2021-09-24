from flask import Flask,request,jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email
from CustomerForm import customerform
from customerUpdateForm import customerupdateform
import sys
sys.path.insert(0, '../database')
from dbConnection import connect
from dbTablesCreation import CreateTables
app=Flask(__name__)
conn=connect(app)
cur=conn.cursor()
CreateTables(conn,cur)

@app.route('/customers', methods=['POST'])
def add_customer():
    try:
       form=customerform(request.form)
       if form.validate():
           if request.form['image']=="":
               image='default.png'
           else:
               image=request.form['image']
           customerData={
               'name':request.form['name'],
               'email':request.form['email'],
               'phone':request.form['phone'],
               'image':image,
               'password':request.form['password']
                 }
         
           value=(request.form['name'],request.form['email'],request.form['phone'],request.form['image'],
                hash(request.form['password']))
          
           sql='INSERT Into `customers`(`name`,`email`,`phone`,`image`,`password`)  values ' + str(value)
           cur.execute(sql)
           conn.commit()
           return jsonify({
                  'success':True,
                  'details':[{'customerData':customerData}],
                  'status':200,
                   'message':'User has been successfully added.'}) 
       else:
           return jsonify({
                  'success':False,
                  'details':[],
                  'status':400,
                   'message':'validation Error'
                            })
    except:
         return jsonify({
                  'success':False,
                  'details':[],
                  'status':500,
                   'message':'Server errpr'
                            })
@app.route('/customers/<customerid>', methods=['get'])
def get_customer(customerid):
    try:
       customer=cur.execute('SELECT * FROM `customers` where id=' +(customerid))
       conn.commit()
       if customer:
           customerData=cur.fetchone()
           customerDetails={
               'name':customerData[1],
               'email':customerData[3],
               'phone':customerData[2],
               'image':customerData[4]
                 }
           return jsonify({
                  'success':True,
                  'details':[{'customerData':customerDetails}],
                  'status':200,
                   'message':'customer has been retreieved successfully.'}) 
       else:
           return jsonify({
                  'success':False,
                  'details':[],
                  'status':404,
                   'message':"customer doesn't exist"
                            })
    except:
         return jsonify({
                  'success':False,
                  'details':[],
                  'status':500,
                   'message':'Server errpr'
                            })

@app.route('/customers/<customerid>', methods=['delete'])
def delete_customer(customerid):
    try:
       customer=cur.execute('SELECT * FROM `customers` where id=' +(customerid))
       conn.commit()
       if customer:
           cur.execute('DELETE  FROM `customers` where id=' +(customerid))
           conn.commit()
           return jsonify({
                  'success':True,
                  'details':[],
                  'status':200,
                   'message':'customer has been  successfully DELETED.'}) 
       else:
           return jsonify({
                  'success':False,
                  'details':[],
                  'status':404,
                   'message':"customer doesn't exist"
                            })
    except:
         return jsonify({
                  'success':False,
                  'details':[],
                  'status':500,
                   'message':'Server errpr'
                            })
'''TO unify the way we receive data we will use from but we may use json
and beacuse of the form we can't user put or patch'''

@app.route('/customers/<customerid>', methods=['post'])
def update_customer(customerid):
        # try:
             customer=cur.execute('SELECT * FROM `customers` where id=' +(customerid))
             conn.commit()
             if customer:
                  customerData=cur.fetchone()
                  form=customerupdateform(request.form)
                  if form.validate(): 

                       if ('image' in request.form) and request.form['image']!="" :
                              image=request.form['image']
                       else:
                              image=customerData[4]
                       sql='update `customers` set '
                       for key in request.form:
                           sql+="`"+key+"` = '"+str(request.form[key])+"',"
                       l=len(sql)
                       mysql=sql[:l-1]
                       mysql+=' where id='+customerid
 
                       cur.execute(mysql)
                       conn.commit()
                       return jsonify({
                            'success':True,
                             'details':[],
                              'status':200,
                              'message':'customer has been  successfully updated.'}) 
                  else:
                       return jsonify({
                            'success':False,
                            'details':[],
                            'status':400,
                            'message':'validation Error'
                             })
             else:
                   return jsonify({
                         'success':False,
                          'details':[],
                          'status':404,
                           'message':"customer doesn't exist"
                            })
        # except:
                # return jsonify({
                #        'success':False,
                #        'details':[],
                #         'status':500,
                #          'message':'Server errpr'
                #             })
    # try:
    #    customer=cur.execute('SELECT * FROM `customers` where id=' +(customerid))
    #    form=customerform(request.form)
    #    if form.validate():
    #        if request.form['image']=="":
    #            image='default.png'
    #        else:
    #            image=request.form['image']
    #        customerData={
    #            'name':request.form['name'],
    #            'email':request.form['email'],
    #            'phone':request.form['phone'],
    #            'image':image,
    #            'password':request.form['password']
    #              }
         
    #        value=(request.form['name'],request.form['email'],request.form['phone'],request.form['image'],
    #             hash(request.form['password']))
          
    #        sql='INSERT Into `customers`(`name`,`email`,`phone`,`image`,`password`)  values ' + str(value)
    #        cur.execute(sql)
    #        conn.commit()
    #        return jsonify({
    #               'success':True,
    #               'details':[{'customerData':customerData}],
    #               'status':200,
    #                'message':'User has been successfully added.'}) 
    #    else:
    #        return jsonify({
    #               'success':False,
    #               'details':[],
    #               'status':400,
    #                'message':'validation Error'
    #                         })
    # except:
    #      return jsonify({
    #               'success':False,
    #               'details':[],
    #               'status':500,
    #                'message':'Server errpr'
    #                         })    
    


if __name__ == '__main__':
    app.run(debug=True)