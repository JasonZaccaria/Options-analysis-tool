from flask import Flask, redirect, url_for, render_template, request, session, flash
import requests
import expected_move
import os
app = Flask(__name__)
app.secret_key = os.getenv('secret_key')
 
@app.route('/')
def home():
    data = [
        ('2021-01-01', 0),
        ('2021-01-01', 0),
        ('2021-01-01', 0),
        ('2021-01-01', 0),
        ('2021-01-01', 0),
        ('2021-01-01', 0),
        ('2021-01-01', 0),
    ]
    labels = [row[0] for row in data]
    values = [row[1] for row in data]
    return render_template('index.html', labels=labels, values=values)

@app.route('/ticker', methods=['POST', 'GET'])
def ticker():
    if request.method == 'POST':
        try:
            ticker = request.form.get('tick')
            #session['ticker'] = ticker
            dn = request.form.get('options')
            data = expected_move.OPTIONS_PROBABILITY_CONE(ticker, dn)
            data = data.graph()
        
            labels = data['exp_dates'].to_list()
            values = data['higher'].to_list()
            values_2 = data['lower'].to_list()
        
            quotes = expected_move.OPTIONS_PROBABILITY_CONE(ticker, dn)
            quotes = quotes.quotes()

            table_headers = ['Expiration Dates']
            if dn == 'None':
                table_headers.extend(['1 stdv higher', '1 stdv lower'])
                tuple(table_headers)
            
            elif dn =='2':
                table_headers.extend(['2 stdv higher', '2 stdv lower'])
                tuple(table_headers)
            
            elif dn == '3':
                table_headers.extend(['3 stdv higher', '3 stdv lower'])
                tuple(table_headers)
            
            table_list = data.values.tolist()

        except KeyError:
            flash('Incorrect ticker please try again!', 'info')
            return redirect('/')
        
        return render_template('second.html', labels=labels, values=values, values_2=values_2, dn=dn, ticker=ticker, quotes=quotes, table_headers=table_headers, table_list=table_list)
    return render_template('index.html')


@app.route('/chart')
def chart():
    return render_template('chart.html')
 
@app.route('/testing')
def testing():
    blank = [1, 2, 3, 4, 5]
    return render_template('base.html', blank=blank)

@app.route('/num', methods=['POST', 'GET'])
def wow():
    if request.method == 'POST':
        dn = request.form.get('options')
        return render_template('second.html', dn=dn)
    return render_template('second.html')
 
if __name__ == '__main__':
    app.run(debug=True)