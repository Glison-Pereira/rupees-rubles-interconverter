from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *

def mtov():
	mw.withdraw()
	vw.deiconify()
def vtom():
	vw.withdraw()
	mw.deiconify()

def save(id):
	money=ent_money.get()
	if money.strip()=="":
		showerror("Issue","Don't leave Blank Spaces")
		ent_money.delete(0,END)
		ent_money.focus()
	elif len(money)>7:
		showerror("Issue","You have exceeded limit")
		ent_money.delete(0,END)
		ent_money.focus()
	elif not(money.isdigit()): # isnumeric(),re.match(pattern,input string)->import re can also be used
		showerror("Issue","You should enter numbers only")
		ent_money.delete(0,END)
		ent_money.focus()
	else:
		money=int(money)
		if money<1:
			showerror("Issue","Atleast enter 1 and not less than 1")
			ent_money.delete(0,END)
			ent_money.focus()
		else:
			con=None
			try:
				con=connect("database_name.db")
				cursor=con.cursor()
				sql="insert into table_name values('%f','%s')"
				if id==1:
					ru=money*0.90
					stry=u'\u20B9'
				elif id==2:
					ru=money*1.11
					stry=u'\u20BD'	
				cursor.execute(sql % (ru,stry))
				con.commit()   
				showinfo("Success",str(ru)+" "+stry)
				ent_money.delete(0,END)
				ent_money.focus()
			except Exception as e:
				showerror("Issue ",e)
				con.rollback()
			finally:
				if con is not None:
					con.close()	

def view():
	con=None
	try:
		con=connect("database_name.db")
		cursor=con.cursor()
		sql="select * from table_name"
		cursor.execute(sql)
		data=cursor.fetchall()
		for d in data:
			ent_scroll.insert(END,str(d)+'\n')
	except Exception as e:
		showerror("Issue ",e)
		con.rollback()
	finally:
		if con is not None:
			con.close()

def delete():
	con=None
	try:
		con=connect("database_name.db")
		cursor=con.cursor()
		sql="delete from table_name"
		cursor.execute(sql)
		con.commit()
		ent_scroll.delete("1.0",END)
		showinfo("Success","History Deleted Successfully")
	except Exception as e:
		showerror("Issue ",e)
		con.rollback()
	finally:
		if con is not None:
			con.close()

mw=Tk()
mw.title("Rupees-Ruble InterConverter")
mw.geometry("650x500+50+50")
mw.configure(bg="aquamarine")

f=("Algerian",20,"bold")

lab_head=Label(mw,text="Welcome to Rupees-Ruble InterConverter",font=f,bg="aquamarine",fg="green")
lab_head.pack(pady=20)

lab_money=Label(mw,text="Enter your Money here:",font=f,bg="aquamarine",fg="green")
ent_money=Entry(mw,font=f)
lab_money.pack(pady=20)
ent_money.pack(pady=0)

btn_rptorb=Button(mw,text="Rupees to Rubles",font=f,bg="black",fg="white",command=lambda:save(1))
btn_rbtorp=Button(mw,text="Rubles to Rupees",font=f,bg="black",fg="white",command=lambda:save(2))
btn_view=Button(mw,text="Go to View",font=f,bg="black",fg="white",command=mtov)
btn_rptorb.place(x=200,y=200)
btn_rbtorp.place(x=200,y=270)
btn_view.place(x=250,y=350)

vw=Toplevel(mw)
vw.title("Rupees-Ruble InterConverter")
vw.geometry("650x500+50+50")
vw.configure(bg="aquamarine")

btn_back=Button(vw,text="Back to Enter Money",font=f,bg="black",fg="white",command=vtom)
btn_delete=Button(vw,text="Delete History",font=f,bg="black",fg="white",command=delete)
btn_history=Button(vw,text="View History",font=f,bg="black",fg="white",command=view)

btn_history.place(x=100,y=40)
btn_back.place(x=150,y=120)
btn_delete.place(x=350,y=40)

ent_scroll=ScrolledText(vw,font=f,width=25,height=10)
ent_scroll.place(x=100,y=180)

vw.withdraw()

mw.mainloop()