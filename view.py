import pandas as pd

classes = ['Animal', 'Peleas', 'Fantasia', '4 paneles', 'Drama Histórico', 'Terror', 'Humor', 'Romance',
           'Comedia romántica', 'Ciencia ficción', 'Deportes', 'Suspenso']

gt_df = pd.read_csv('./mangalabels.csv', usecols=[2,3,4,5,6,7,8,9,10,11,12,13])
ground_truth = gt_df.values
gt_sum = gt_df.sum()
pt_df = pd.read_csv("./predicted.csv", header=None)
predicted = pt_df.values
pt_sum = pt_df.sum()

for i

