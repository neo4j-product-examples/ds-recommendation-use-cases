import pandas as pd


def agg_labels(df, cls_col, label_col, top_n=2):
    df.user_segment = ''
    cls_list = df[cls_col].unique()
    for cls in cls_list:
        labels = df.loc[df[cls_col] == cls, label_col].explode().value_counts(ascending=False).index[:top_n].tolist()
        labels.sort()
        label = ' & '.join(labels)
        df.loc[df[cls_col] == cls, 'user_segment'] = label