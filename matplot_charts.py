import base64
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np

colors = ['#4dc9f6', '#f67019', '#f53794', '#537bc4', '#acc236', '#166a8f',
          '#00a950', '#58595b', '#8549ba', '#e6194b', '#3cb44b', '#ffe119',
          '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c',
          '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000',
          '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#ffffff',
          '#000000']
#plt.style.use('_mpl-gallery-nogrid')

def make_pie_chart(amount_acc_list):
    amounts = [amount_acc[0] for amount_acc in amount_acc_list]
    labels = [amount_acc[1] for amount_acc in amount_acc_list]

    # plot
    fig, ax = plt.subplots()
    ax.pie(amounts, labels=labels,
           wedgeprops={"linewidth": 1, "edgecolor": "white"})

    #plt.show()
    buffer = BytesIO()
    plt.gcf().set_size_inches(5, 3)
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    plt.clf()
    return graphic

# make line charts for monthly trends.
# Input is list of array of length 12 and title.
def make_line_chart_monthly_trends(monthly_data_list, title):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
              'Oct', 'Nov', 'Dec']
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for year in monthly_data_list:
        amounts = monthly_data_list[year]
        plt.plot(months, amounts, label=year)
        #for i,j in zip(months, amounts):
        #    ax.annotate(str(j),xy=(i,j))

    plt.legend()
    plt.title(title)


    #plt.show()
    buffer = BytesIO()
    plt.gcf().set_size_inches(8, 4)
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    plt.clf()
    return graphic
