import sqlite3

def view_sample_data():
    # 连接到SQLite数据库
    conn = sqlite3.connect('../travel.db')
    cursor = conn.cursor()
    
    # 查看t_applicationmodel表中的数据
    cursor.execute("SELECT * FROM t_applicationmodel LIMIT 2;")
    applications = cursor.fetchall()
    
    print("请假申请表 (t_applicationmodel) 示例数据:")
    print("申请人\t天数\t类型\t开始日期\t结束日期\t状态\t原因")
    for app in applications:
        print(f"{app[0]}\t{app[1]}\t{app[2]}\t{app[3]}\t{app[4]}\t{app[7]}\t{app[8]}")
    
    print("\n" + "="*50 + "\n")
    
    # 查看t_rolemodel表中的数据
    cursor.execute("SELECT * FROM t_rolemodel;")
    roles = cursor.fetchall()
    
    print("角色表 (t_rolemodel) 数据:")
    print("ID\t名称\t\t备注")
    for role in roles:
        print(f"{role[1]}\t{role[0]}\t\t{role[4]}")
    
    conn.close()

if __name__ == "__main__":
    view_sample_data()