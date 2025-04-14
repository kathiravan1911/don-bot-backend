
import pandas as pd

def get_ai_suggestion_dict(file_path="backtest_data.csv"):
    df = pd.read_csv(file_path)
    summary = df.groupby('Symbol')['Outcome'].value_counts().unstack().fillna(0)
    summary['Total'] = summary.sum(axis=1)
    summary['SuccessRate'] = (summary['Target'] / summary['Total']) * 100
    summary['AI_Suggestion'] = summary['SuccessRate'].apply(lambda x: '✅ High Chance' if x >= 60 else '❌ Low Chance')
    return summary[['SuccessRate', 'AI_Suggestion']].to_dict(orient='index')
