import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

df = pd.DataFrame(np.random.random((10,3)), columns = ("col 1", "col 2", "col 3"))


fig, ax =plt.subplots(figsize=(8.27,11.69)) #A4 Size
ax.axis('tight')
ax.axis('off')
the_table = ax.table(cellText=df.values,colLabels=df.columns,loc='upper left')
plt.text(0.05,0.95,"Hello World and this is ", transform=fig.transFigure, size=24) #Text


pp = PdfPages("foo.pdf") #PDF Name
pp.savefig(fig, bbox_inches='tight')
pp.close()