#1. Test di Significatività Statistica (Z-Test):

# Task: Calcola il p-value per le conversioni tra A e B. Se il p-value è < 0.05, puoi rigettare l'ipotesi nulla?

from datasets.exceptions import DefunctDatasetError
import scipy.stats as stats
from scipy.stats import chi2_contingency
# Importing Libraries
import ast
import numpy as np
import pandas as pd
from datasets import load_dataset
import matplotlib.pyplot as plt
import seaborn as sns # Import seaborn for enhanced plotting


df = pd.read_csv('ab_testing.csv')
df=df.dropna(how='all')
df.set_index('User_ID',inplace=True)
contingency_table = pd.crosstab(df['Group_test'], df['Conv'])
#Ipotesi nulla che le conversioni siano le stesse nei due gruppi
chi2, p, dof, expected = chi2_contingency(contingency_table)
alpha = 0.05
print(f"Risultati del Test Chi-quadro")
print(f"Statistica Chi2: {chi2:.4f}")
print(f"p-value: {p:.4f}")

if p < alpha:
    print(f"\nRISULTATO: Significativo (p < {alpha})")
else:
    print(f"\nRISULTATO: Non Significativo (p >= {alpha})")



# 2. Intervalli di Confidenza al 95%:

# Task: Calcola e visualizza (con barre d'errore) gli intervalli di confidenza per i tassi di conversione di entrambi i gruppi. C'è un overlap?


df = pd.read_csv('ab_testing.csv')
df=df.dropna(how='all')
df.set_index('User_ID',inplace=True)
a=df.loc[df['Group_test']=='A','Conv']
b=df.loc[df['Group_test']=='B','Conv']

ta=len(a[a=='Yes'])/len(a)
tb=len(b[b=='Yes'])/len(b)
diff=tb-ta
se = np.sqrt((ta* (1 - ta) / len(a)) + (tb * (1 - tb) / len(b)))
z_critical = stats.norm.ppf(0.975) 
moe = z_critical * se

ci_lower = diff - moe
ci_upper = diff + moe
print(f"Intervallo di Confidenza 95%: [{ci_lower:.2%}, {ci_upper:.2%}]")


# 3.
# Analisi della Distribuzione (Engagement):

# Task: Crea un istogramma o un KDE Plot per confrontare la distribuzione di Time Spent tra i due gruppi. Il cambiamento ha spostato la media o ha creato più utenti "alto-spendenti"?


df = pd.read_csv('ab_testing.csv')
df=df.dropna(how='all')
df.set_index('User_ID',inplace=True)
a=df.loc[df['Group_test']=='A','Time_Spent']
b=df.loc[df['Group_test']=='B','Time_Spent']

fig, axes = plt.subplots(1, 2, figsize=(14, 5)) # Create a figure with 2 subplots

# Plot for Group A
a.plot(kind='hist', bins=30, edgecolor='black', color='skyblue', alpha=0.7, ax=axes[0])
axes[0].set_title('Histogram of Time Spent for Group A')
axes[0].set_xlabel('Time Spent (minutes)')
axes[0].set_ylabel('Frequency')
mean_a = a.mean()
axes[0].axvline(mean_a, color='blue', linestyle='dashed', linewidth=2, label=f'Mean: {mean_a:.2f}')
axes[0].legend()

# Plot for Group B
b.plot(kind='hist', bins=30, edgecolor='black', color='red', alpha=0.7, ax=axes[1])
axes[1].set_title('Histogram of Time Spent for Group B')
axes[1].set_xlabel('Time Spent (minutes)')
axes[1].set_ylabel('Frequency')
mean_b = b.mean()
axes[1].axvline(mean_b, color='darkred', linestyle='dashed', linewidth=2, label=f'Mean: {mean_b:.2f}')
axes[1].legend()

plt.tight_layout() # Adjust layout to prevent overlapping titles/labels
plt.show()


# 4. Segmentazione e Simpson's Paradox:

# Task: Crea un grafico a barre che mostri il Conversion Rate per Gruppo, ma suddiviso per Device. È possibile che B vinca globalmente ma perda su Desktop? (Analisi dei bias).



df = pd.read_csv('ab_testing.csv')
df=df.dropna(how='all')
df.set_index('User_ID',inplace=True)
a=df.loc[df['Group_test']=='A',['Conv','Device']]
b=df.loc[df['Group_test']=='B',['Conv','Device']]

# Count total users per device in each group
conta = a['Device'].value_counts()
contb = b['Device'].value_counts()

# Count converted users per device in each group
conva = a[a['Conv']=='Yes'].groupby('Device').size()
convb = b[b['Conv']=='Yes'].groupby('Device').size()

# Calculate conversion rates for Group A
conversion_rate_a = (conva / conta) * 100
print('Conversion Rate for Group A (by Device):')
display(conversion_rate_a.fillna(0).round(2))

print('\nConversion Rate for Group B (by Device):')
# Calculate conversion rates for Group B
conversion_rate_b = (convb / contb) * 100
display(conversion_rate_b.fillna(0).round(2))


# Combine conversion rates into a single DataFrame for plotting
conversion_rates_df = pd.DataFrame({
    'Device': conversion_rate_a.index.tolist() * 2,
    'Conversion Rate': conversion_rate_a.tolist() + conversion_rate_b.tolist(),
    'Group': ['A'] * len(conversion_rate_a) + ['B'] * len(conversion_rate_b)
})

# Create the bar plot
plt.figure(figsize=(10, 6))
sns.barplot(x='Device', y='Conversion Rate', hue='Group', data=conversion_rates_df, palette='viridis')
plt.title('Conversion Rate by Device for Group A vs. Group B')
plt.xlabel('Device Type')
plt.ylabel('Conversion Rate (%)')
plt.ylim(0, 20) # Set a reasonable y-limit based on the calculated rates
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()