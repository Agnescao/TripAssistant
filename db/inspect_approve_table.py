import sqlite3

def inspect_approve_table():
    # 连接到SQLite数据库
    conn = sqlite3.connect('../travel.db')
    cursor = conn.cursor()
    
    # 检查表是否存在
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='t_approverecodemodel';")
    result = cursor.fetchone()
    
    if result is None:
        print("t_approverecodemodel 表不存在于数据库中")
        return
    
    print("t_approverecodemodel 表存在")
    print("="*50)
    
    # 查看t_approverecodemodel表结构
    cursor.execute("PRAGMA table_info(t_approverecodemodel);")
    columns = cursor.fetchall()
    
    print("\nt_approverecodemodel 表结构:")
    print("序号\t名称\t\t\t数据类型\t非空\t默认值\t主键")
    for column in columns:
        print(f"{column[0]}\t{column[1]}\t\t\t{column[2]}\t{column[3]}\t{column[4]}\t{column[5]}")
    
    print("\n" + "="*60 + "\n")
    
    # 查看t_approverecodemodel表中的数据
    cursor.execute("SELECT * FROM t_approverecodemodel;")
    rows = cursor.fetchall()
    
    if len(rows) == 0:
        print("t_approverecodemodel 表中没有数据")
    else:
        print("t_approverecodemodel 表数据:")
        column_names = [column[1] for column in columns]
        print("\t".join(column_names))
        print("-" * 80)
        for row in rows:
            print("\t".join(str(item) for item in row))
    
    conn.close()

if __name__ == "__main__":
    inspect_approve_table()