import sqlite3

def check_all_tables():
    # 连接到SQLite数据库
    conn = sqlite3.connect('../travel.db')
    cursor = conn.cursor()
    
    # 查询所有表名
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("数据库中的所有表:")
    for i, table in enumerate(tables, 1):
        print(f"{i}. {table[0]}")
        
        # 查询每个表的记录数
        cursor.execute(f"SELECT COUNT(*) FROM {table[0]};")
        count = cursor.fetchone()[0]
        print(f"   记录数: {count}")
    
    conn.close()
    
    # 检查是否存在t_applicationmodel表
    table_names = [table[0] for table in tables]
    if 't_applicationmodel' in table_names:
        print("\n✓ t_applicationmodel 表存在")
    else:
        print("\n✗ t_applicationmodel 表不存在")

if __name__ == "__main__":
    check_all_tables()