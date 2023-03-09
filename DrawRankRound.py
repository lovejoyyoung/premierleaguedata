import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read CSV file
df = pd.read_csv('./data/ToT_FC_RankAfterroundClean.csv')

# Grab colume data
x = df['Round']
y = df['Rank']

# Use the polyfit function to fit the data and 
# generate the coefficients of a polynomial of degree one
p = np.polyfit(x, y, 1)

# Utilize poly1d function to generates 
# a polynomial object from the polynomial coefficients
trendline = np.poly1d(p)

# Draw 
plt.plot(x, y, '')
plt.plot(x, trendline(x))

plt.xlim(1, max(x))
plt.ylim(max(y)+1, min(y)-1)

# plt.ylim(max(y)+1, min(y)-1)

# Tag title and XY axis
plt.title('Trendline')
plt.xlabel('Round')
plt.ylabel('Rank')

# Show 
plt.show()
