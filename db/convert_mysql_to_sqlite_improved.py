import sqlite3
import re

def convert_mysql_to_sqlite(mysql_file, sqlite_file):
    # 读取MySQL SQL文件
    with open(mysql_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # 移除注释
    sql_content = re.sub(r'/\*.*?\*/', '', sql_content, flags=re.DOTALL)
    sql_content = re.sub(r'--.*', '', sql_content)
    
    # 移除MySQL特有的语句
    sql_content = re.sub(r'SET NAMES .*?;', '', sql_content)
    sql_content = re.sub(r'SET FOREIGN_KEY_CHECKS = 0;', '', sql_content)
    sql_content = re.sub(r'SET FOREIGN_KEY_CHECKS = 1;', '', sql_content)
    
    # 移除反引号
    sql_content = sql_content.replace('`', '')
    
    # 转换数据类型
    sql_content = re.sub(r'int\(0\)', 'INTEGER', sql_content)
    sql_content = re.sub(r'datetime\(0\)', 'DATETIME', sql_content)
    sql_content = re.sub(r'varchar\((\d+)\)', r'VARCHAR(\1)', sql_content)
    sql_content = re.sub(r'tinyint\(1\)', 'BOOLEAN', sql_content)
    
    # 处理表定义
    # 移除ENGINE, CHARACTER SET, COLLATE, ROW_FORMAT等MySQL特定选项
    sql_content = re.sub(r'ENGINE.*?(?=;)', '', sql_content)
    sql_content = re.sub(r'CHARACTER SET .*?(?=,|;)', '', sql_content)
    sql_content = re.sub(r'COLLATE .*?(?=,|;)', '', sql_content)
    sql_content = re.sub(r'ROW_FORMAT .*?(?=,|;)', '', sql_content)
    
    # 处理AUTO_INCREMENT
    sql_content = re.sub(r'AUTO_INCREMENT = \d+ ', '', sql_content)
    sql_content = re.sub(r'AUTO_INCREMENT\d*', '', sql_content)
    
    # 处理索引定义
    sql_content = re.sub(r'USING BTREE', '', sql_content)
    sql_content = re.sub(r'INDEX .*?\).*?(?=,|;)', '', sql_content)
    sql_content = re.sub(r',\s*\)', ')', sql_content)
    
    # 处理外键约束
    sql_content = re.sub(r'CONSTRAINT .*? FOREIGN KEY .*?(?=,|;)', '', sql_content)
    sql_content = re.sub(r',\s*\)', ')', sql_content)
    
    # 处理COMMENT
    sql_content = re.sub(r'COMMENT .*?(?=,|;)', '', sql_content)
    
    # 处理PRIMARY KEY定义中的USING BTREE
    sql_content = re.sub(r'PRIMARY KEY .*? USING BTREE', 'PRIMARY KEY', sql_content)
    
    # 分割SQL语句
    statements = re.split(r';\s*\n', sql_content)
    
    # 创建SQLite连接
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    
    # 执行每个SQL语句
    for statement in statements:
        statement = statement.strip()
        if statement and not statement.startswith('--') and not statement.startswith('/*') and statement != '':
            try:
                # 特殊处理CREATE TABLE语句，确保语法正确
                if statement.startswith('CREATE TABLE'):
                    # 移除可能的多余逗号
                    statement = re.sub(r',\s*\)', ')', statement)
                
                cursor.execute(statement)
                print(f"执行成功: {statement[:50]}...")
            except Exception as e:
                print(f"执行失败: {statement[:50]}... 错误: {str(e)}")
    
    # 提交更改并关闭连接
    conn.commit()
    conn.close()
    
    print(f"SQLite数据库已创建: {sqlite_file}")

if __name__ == "__main__":
    mysql_file = "../travel.sql"
    sqlite_file = "../travel.db"
    convert_mysql_to_sqlite(mysql_file, sqlite_file)