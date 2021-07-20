from flask import Flask , render_template

app=Flask(__name__)

@app.route('/plot/')
def plot():
    from pandas_datareader import data
    import datetime
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN

    start=datetime.datetime(2020,12,1)
    end=datetime.datetime(2021,2,1)

    df=data.DataReader(name="GOOG",data_source="yahoo",start=start,end=end)
    def inc_dec(c,o):
        if c>o:
            value="Increase"
        elif c<o:
            value="Decrease"
        else:
            value="Equal"
        return value
    df["Status"]=[inc_dec(c,o) for c,o in zip(df.Close,df.Open)]
    df["Middle"]=(df.Open+df.Close)/2
    df["Height"]=abs(df.Open-df.Close)
    p=figure(x_axis_type='datetime',width=1800,height=800 , title="Candlestick Chart", sizing_mode='scale_width')
    p.grid.grid_line_alpha=0.8
    p.segment(df.index,df.High,df.index,df.Low,color="black")
    hours_12=12*20*60*1000
    p.rect(df.index[df.Status=="Increase"] , df.Middle[df.Status=="Increase"] ,
           hours_12, df.Height[df.Status=="Increase"] , fill_color="#B0E0E6",line_color="black" )
    p.rect(df.index[df.Status=="Decrease"] , df.Middle[df.Status=="Decrease"]  ,
           hours_12, df.Height[df.Status=="Decrease"]  , fill_color="#8B0000" , line_color="black" )

    script1,div1=components(p)
    cdn_js=CDN.js_files[0]

    return render_template("plot.html",script1=script1,div1=div1,cdn_js=cdn_js)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
