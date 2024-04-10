import pickle
import pandas as pd

ION_CHANNEL = 19
for i in range(ION_CHANNEL):
    with open('saved_bar_chart_1'+str(i)+'.pkl', 'rb') as f:
        loaded_dict = pickle.load(f)

    zf = []
    for key, value in loaded_dict.items():
        temp = dict({"Region": [], "value": []})
        for k,v in value.items():
            temp["Region"].append(k)
            temp["value"].append(abs(v))

        df = pd.DataFrame.from_dict(temp)
        zf.append(df)
    print(zf[0])



    ax = df.plot.bar(x='Region', y='value')
    ax.figure.savefig("demo"+str(i)+".png")
