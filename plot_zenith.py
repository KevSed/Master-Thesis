import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('build/runs.csv')


plt.hist(df.zenith, weights=df.ontime / 3600, bins=20, range=[0, 30])
plt.xlabel(r'$\theta / \textdegree$')
plt.ylabel(r'Observation Time / h')

plt.tight_layout(pad=0)
plt.savefig('Plots/zenith.pdf')
