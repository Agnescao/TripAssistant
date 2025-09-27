import sqlite3
import re

def clean_sql_content(sql_content):
    """清理SQL内容，移除MySQL特有语法并转换为SQLite兼容格式"""
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
    
    # 移除MySQL特定的表选项
    sql_content = re.sub(r'ENGINE.*?(?=;)', '', sql_content)
    sql_content = re.sub(r'CHARACTER SET .*?(?=,|;)', '', sql_content)
    sql_content = re.sub(r'COLLATE .*?(?=,|;)', '', sql_content)
    sql_content = re.sub(r'ROW_FORMAT .*?(?=,|;)', '', sql_content)
    sql_content = re.sub(r'USING BTREE', '', sql_content)
    
    # 处理AUTO_INCREMENT
    sql_content = re.sub(r'AUTO_INCREMENT = \d+ ', '', sql_content)
    sql_content = re.sub(r'AUTO_INCREMENT\d*', '', sql_content)
    
    # 处理注释
    sql_content = re.sub(r'COMMENT .*?(?=,|;)', '', sql_content)
    
    # 处理索引和外键定义（SQLite不支持在CREATE TABLE中定义外键约束）
    sql_content = re.sub(r',\s*CONSTRAINT .*?(?=,|;)', '', sql_content)
    sql_content = re.sub(r',\s*INDEX .*?(?=,|;)', '', sql_content)
    sql_content = re.sub(r',\s*FOREIGN KEY .*?(?=,|;)', '', sql_content)
    sql_content = re.sub(r',\s*UNIQUE INDEX .*?(?=,|;)', '', sql_content)
    
    # 清理可能产生的多余逗号
    sql_content = re.sub(r',\s*\)', ')', sql_content)
    
    return sql_content

def extract_sql_statements(sql_content):
    """提取独立的SQL语句"""
    statements = []
    # 按分号分割语句
    raw_statements = re.split(r';\s*\n', sql_content)
    
    for statement in raw_statements:
        statement = statement.strip()
        if statement and not statement.startswith('--') and not statement.startswith('/*') and statement != '':
            statements.append(statement)
    
    return statements

def convert_mysql_to_sqlite(mysql_file, sqlite_file):
    """将MySQL SQL文件转换为SQLite数据库"""
    # 读取MySQL SQL文件
    with open(mysql_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # 清理SQL内容
    cleaned_sql = clean_sql_content(sql_content)
    
    # 提取SQL语句
    statements = extract_sql_statements(cleaned_sql)
    
    # 创建SQLite连接
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    
    # 执行每个SQL语句
    successful_tables = []
    failed_statements = []
    
    for statement in statements:
        try:
            cursor.execute(statement)
            if statement.startswith('CREATE TABLE'):
                # 提取表名
                table_name = re.search(r'CREATE TABLE (\w+)', statement)
                if table_name:
                    successful_tables.append(table_name.group(1))
            print(f"成功执行: {statement[:50]}...")
        except Exception as e:
            if statement.startswith('CREATE TABLE'):
                table_name = re.search(r'CREATE TABLE (\w+)', statement)
                if table_name:
                    print(f"创建表失败 {table_name.group(1)}: {str(e)}")
                    failed_statements.append((statement, str(e)))
            elif statement.startswith('INSERT INTO'):
                print(f"插入数据失败: {statement[:50]}... 错误: {str(e)}")
                failed_statements.append((statement, str(e)))
            else:
                print(f"执行失败: {statement[:50]}... 错误: {str(e)}")
                failed_statements.append((statement, str(e)))
    
    # 提交更改并关闭连接
    conn.commit()
    conn.close()
    
    print(f"\n成功创建的表:")
    for table in successful_tables:
        print(f"  - {table}")
    
    print(f"\nSQLite数据库已创建: {sqlite_file}")
    
    if failed_statements:
        print(f"\n失败的语句数量: {len(failed_statements)}")
    
    return len(successful_tables)

if __name__ == "__main__":
    mysql_file = "../travel.sql"
    sqlite_file = "travel_complete.db"
    convert_mysql_to_sqlite(mysql_file, sqlite_file)