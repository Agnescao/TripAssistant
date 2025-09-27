import sqlite3

def check_database():
    # 连接到SQLite数据库
    conn = sqlite3.connect('../travel.db')
    cursor = conn.cursor()
    
    # 查询所有表名
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("数据库中的表:")
    for table in tables:
        print(f"- {table[0]}")
        
        # 查询每个表的记录数
        cursor.execute(f"SELECT COUNT(*) FROM {table[0]};")
        count = cursor.fetchone()[0]
        print(f"  记录数: {count}")
        
        # 显示表的结构
        cursor.execute(f"PRAGMA table_info({table[0]});")
        columns = cursor.fetchall()
        print("  字段:")
        for column in columns:
            print(f"    {column[1]} ({column[2]})")
        print()
    
    conn.close()

if __name__ == "__main__":
    check_database()