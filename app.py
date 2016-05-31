from flask import Flask, render_template, request, redirect
import pandas as pd
from bokeh.plotting import figure,output_file,show
from bokeh.embed import components


app = Flask(__name__)

app.vars = {}

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index',methods = ['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        app.vars['ticker'] = request.form['ticker']
        app.vars['open'] = request.form.get('open')
        app.vars['close'] = request.form.get('close')
        app.vars['adjopen'] = request.form.get('adjopen')
        app.vars['adjclose'] = request.form.get('adjclose')
        return redirect('/graph')
        

@app.route('/graph',methods = ['GET','POST'])
def graph():
    if request.method == 'GET':
        url = 'https://www.quandl.com/api/v3/datasets/WIKI/'+app.vars['ticker']+'.csv'
        #f = open('%s.txt'%(app.vars['ticker']),'w')
        #f.write('url: %s\n'%url)
        #f.close()
        df = pd.read_csv(url)
        df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
        prices = df[['Date','Open','Close','Adj. Open', 'Adj. Close']]
        
        p = figure(title = 'Stock prices for '+app.vars['ticker'], x_axis_type = 'datetime', 
                   x_axis_label='Date', y_axis_label='Price', plot_width=1000)
        
        if app.vars['open']:
            p.line(prices['Date'],prices['Open'],line_width=2,legend='Open',color='green')
        if app.vars['close']:
            p.line(prices['Date'],prices['Close'],line_width=2,legend='Close',color='red')
        if app.vars['adjopen']:
            p.line(prices['Date'],prices['Adj. Open'],line_width=2,legend='Adj. Open', color='blue')
        if app.vars['adjclose']:
            p.line(prices['Date'],prices['Adj. Close'],line_width=2,legend='Adj. Close', color='orange')
        
        script,div = components(p)
        return render_template('graph.html',ticker=app.vars['ticker'],script=script,div=div)
    else:
        return redirect('/index')

if __name__ == '__main__':
    #app.run(debug=True)
    #app.run(host='0.0.0.0')
    app.run(port=33507)
