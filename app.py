from flask import Flask, jsonify
import pandas as pd
from flask_cors import CORS
from ai_suggestions import get_ai_suggestion_dict

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Don Bot API is running 😎"

@app.route('/api/breakouts', methods=['GET'])
def get_breakouts():
    try:
        print("📂 Reading breakout_stocks.csv...")
        df = pd.read_csv("breakout_stocks.csv")
        print("✅ Breakout Data:")
        print(df.head())

        print("🧠 Reading AI Suggestions...")
        ai_dict = get_ai_suggestion_dict("backtest_data.csv")
        print("✅ AI Suggestion Dictionary:")
        print(ai_dict)

        print("🔁 Matching Symbols...")
        def match_ai(symbol):
            for key in ai_dict.keys():
                if symbol in key or key in symbol:
                    return key
            return None

        df['Matched'] = df['Symbol'].apply(match_ai)
        df['SuccessRate'] = df['Matched'].apply(lambda k: round(ai_dict.get(k, {}).get('SuccessRate', 0), 2) if k else 0)
        df['AI_Suggestion'] = df['Matched'].apply(lambda k: ai_dict.get(k, {}).get('AI_Suggestion', '❓ No Data') if k else '❓ No Data')
        df.drop(columns=['Matched'], inplace=True)

        print("📤 Returning response...")
        return jsonify(df.to_dict(orient='records'))

    except Exception as e:
        print("❌ Error occurred in /api/breakouts route:")
        print(e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
