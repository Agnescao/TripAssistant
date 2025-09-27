import sqlite3

# 连接到数据库文件
conn = sqlite3.connect('../travel.db')
cursor = conn.cursor()

# 检查SQLite版本
cursor.execute('SELECT sqlite_version()')
version = cursor.fetchone()[0]
print(f'SQLite version: {version}')

# 列出所有表
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('Tables in database:')
for table in tables:
    print(f'  - {table[0]}')

conn.close()
print('\n文件确认为有效的SQLite数据库格式')