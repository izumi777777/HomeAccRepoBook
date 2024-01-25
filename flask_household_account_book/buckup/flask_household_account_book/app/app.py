# ライブラリ宣言
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

# Flask実行
app = Flask(__name__)

# データベースの作成と接続
conn = sqlite3.connect('家計簿.db')
cursor = conn.cursor()

# 予算管理テーブルの作成
cursor.execute('''
    CREATE TABLE IF NOT EXISTS budget (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT, -- 日付列を追加
        category TEXT,
        amount INTEGER,
        description TEXT
    )
''')

# 変動支出テーブルの作成
cursor.execute('''
    CREATE TABLE IF NOT EXISTS variable_expense (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT, -- 日付列を追加
        category TEXT,
        amount INTEGER,
        description TEXT
    )
''')

# 収入管理テーブル、固定支出テーブル、カテゴリテーブルも同様に作成する

conn.commit()
conn.close()

# トップページの表示
@app.route('/', methods=['GET'])
def top_index():
        # top_indexを表示する
        return render_template('top_index.html')

# 予算設定管理フォームの表示
@app.route('/index2', methods=['GET', 'POST'])
def index2():
    if request.method == 'POST':
        # フォームから受け取ったデータをデータベースに挿入
        budget_data = request.form['budget_data']
        budget_category = request.form['budget_category']
        budget_amount = request.form['budget_amount']
        budget_description = request.form['budget_description']
        
        conn = sqlite3.connect('家計簿.db')
        cursor = conn.cursor()
        
        # 予算設定管理テーブルに挿入
        cursor.execute('''
            INSERT INTO budget (data, category, amount, description)
            VALUES (?, ?, ?, ?)
        ''', (budget_data, budget_category, budget_amount, budget_description))

        conn.commit()
        conn.close()
        
        return redirect(url_for('index2'))

    # データベースから予算設定管理テーブルのデータを取得
    conn = sqlite3.connect('家計簿.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM budget')
    
    expenses = cursor.fetchall()
    
    conn.commit()
    conn.close()
    
    # 予算設定管理テーブルのamount列の合計値を取得
    conn = sqlite3.connect('家計簿.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT sum(amount) FROM budget')
    
    total_amount_result = cursor.fetchone()
    total_amount = total_amount_result[0] if total_amount_result else 0

    
    conn.commit()
    conn.close()
    
    # 予算設定管理テーブルのamount列の固定費の合計値を取得
    conn = sqlite3.connect('家計簿.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT SUM(amount) FROM budget WHERE category = '固定'")
    
    total_fixed_cost_amount_result = cursor.fetchone()
    total_fixed_cost_amount = total_fixed_cost_amount_result[0] if total_fixed_cost_amount_result else 0

    conn.commit()
    conn.close()
    
    # 予算設定管理テーブルのamount列の変動費の合計値を取得
    conn = sqlite3.connect('家計簿.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT SUM(amount) FROM budget WHERE category = '変動'")
    
    total_variable_cost_amount_result = cursor.fetchone()
    total_variable_cost_amount = total_variable_cost_amount_result[0] if total_variable_cost_amount_result else 0

    conn.commit()
    conn.close()

    return render_template('index2.html', expenses=expenses, total_amount=total_amount, total_fixed_cost_amount=total_fixed_cost_amount, total_variable_cost_amount=total_variable_cost_amount)

# 変動支出登録フォームの表示
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # フォームから受け取ったデータをデータベースに挿入
        data = request.form['date']
        category = request.form['category']
        amount = request.form['amount']
        description = request.form['description']

        conn = sqlite3.connect('家計簿.db')
        cursor = conn.cursor()

        # 変動支出テーブルに挿入
        cursor.execute('''
            INSERT INTO variable_expense (date, category, amount, description)
            VALUES (?, ?, ?, ?)
        ''', (data, category, amount, description))

        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
        
    # データベースから変動支出テーブルのデータを取得
    conn = sqlite3.connect('家計簿.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM variable_expense')
    
    expenses = cursor.fetchall()
    
    conn.commit()
    conn.close()
    
    # 変動支出テーブルのamount列の合計値を取得
    conn = sqlite3.connect('家計簿.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT sum(amount) FROM variable_expense')
    
    variable_expense_total_amount_result = cursor.fetchone()
    variable_expense_total_amount = variable_expense_total_amount_result[0] if variable_expense_total_amount_result else 0

    
    conn.commit()
    conn.close()

    return render_template('index.html', expenses=expenses, variable_expense_total_amount=variable_expense_total_amount)

# 変動支出テーブル削除ボタンが押されたときの処理
@app.route('/delete_expense/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    conn = sqlite3.connect('家計簿.db')
    cursor = conn.cursor()

    # 変動支出テーブルから削除
    cursor.execute('DELETE FROM variable_expense WHERE id = ?', (expense_id,))

    conn.commit()
    conn.close()

    # 支出一覧ページへ戻る
    return redirect(url_for('index'))

# 予算設定管理テーブル削除ボタンが押されたときの処理
@app.route('/delete_expense2/<int:expense_id2>', methods=['POST'])
def delete_expense2(expense_id2):
    conn = sqlite3.connect('家計簿.db')
    cursor = conn.cursor()

    # 予算設定管理テーブルから削除
    cursor.execute('DELETE FROM budget WHERE id = ?', (expense_id2,))

    conn.commit()
    conn.close()

    # 予算設定管理ページへ戻る
    return redirect(url_for('index2'))

# ファビコンのハンドラ
@app.route('/favicon.ico')
def favicon():
    return 'favicon.ico'

if __name__ == '__main__':
    app.run(debug=True)