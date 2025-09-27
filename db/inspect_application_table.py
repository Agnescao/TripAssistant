import sqlite3

def inspect_application_table():
    # 连接到SQLite数据库
    conn = sqlite3.connect('../travel.db')
    cursor = conn.cursor()
    
    # 查看t_applicationmodel表结构
    cursor.execute("PRAGMA table_info(t_applicationmodel);")
    columns = cursor.fetchall()
    
    print("t_applicationmodel 表结构:")
    print("序号\t名称\t\t\t数据类型\t非空\t默认值\t主键")
    for column in columns:
        print(f"{column[0]}\t{column[1]}\t\t\t{column[2]}\t{column[3]}\t{column[4]}\t{column[5]}")
    
    print("\n" + "="*60 + "\n")
    
    # 查看t_applicationmodel表中的数据
    cursor.execute("SELECT * FROM t_applicationmodel;")
    rows = cursor.fetchall()
    
    print("t_applicationmodel 表数据:")
    print("ID\t申请人\t\t天数\t类型\t开始日期\t\t结束日期\t\t状态\t原因")
    print("-" * 80)
    for row in rows:
        print(f"{row[10]}\t{row[0]}\t\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[7]}\t{row[8]}")
    
    conn.close()

if __name__ == "__main__":
    inspect_application_table()