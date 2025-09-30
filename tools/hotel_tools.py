from datetime import date, datetime
from typing import Optional, List, Dict, Any

from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig

from tools.dbconnection import dbconnection
from tools.confirmation_tool import generic_confirmation
from tools.checkpoint_manager import checkpoint_manager


@tool
def search_hotels(location: str, checkin_date: date, checkout_date: date, guests: int = 2, rooms: int = 1) -> List[Dict]:
    """
    搜索酒店信息
    
    Args:
        location: 位置
        checkin_date: 入住日期
        checkout_date: 退房日期
        guests: 客人数量
        rooms: 房间数量
        
    Returns:
        酒店列表
    """
    # 这里应该是实际的酒店搜索逻辑
    print(f"搜索酒店: location={location}, checkin_date={checkin_date}, checkout_date={checkout_date}")
    
    # 模拟返回一些酒店数据
    hotels = [
        {
            "hotel_id": "h001",
            "name": "北京国际饭店",
            "location": location,
            "price_per_night": 800,
            "rating": 4.5,
            "available_rooms": 5
        },
        {
            "hotel_id": "h002",
            "name": "北京希尔顿酒店",
            "location": location,
            "price_per_night": 1200,
            "rating": 4.8,
            "available_rooms": 3
        }
    ]
    
    return hotels


@tool
def book_hotel(hotel_id: str, checkin_date: date, checkout_date: date, guests: int, rooms: int, config: RunnableConfig) -> str:
    """
    预订酒店
    
    Args:
        hotel_id: 酒店ID
        checkin_date: 入住日期
        checkout_date: 退房日期
        guests: 客人数量
        rooms: 房间数量
        config: 配置信息
        
    Returns:
        预订结果
    """
    configuration = config.get('configurable', {})
    user_id = configuration.get('user_id', None)
    thread_id = configuration.get('thread_id', 'default_thread')
    if not user_id:
        raise ValueError("User ID is required.")
    
    # 获取酒店信息
    db_conn = dbconnection()
    conn = db_conn.connection
    cursor = db_conn.cursor
    
    query = "SELECT * FROM hotels WHERE hotel_id = ?"
    cursor.execute(query, (hotel_id,))
    hotel = cursor.fetchone()
    
    if not hotel:
        cursor.close()
        conn.close()
        return f"酒店 {hotel_id} 不存在"
    
    column_names = [column[0] for column in cursor.description]
    hotel_dict = dict(zip(column_names, hotel))
    
    # 请求用户确认预订操作
    confirmation_message = f"确认预订酒店: {hotel_dict['name']} 从 {checkin_date} 到 {checkout_date}?"
    operation_details = {
        "hotel_id": hotel_id,
        "hotel_name": hotel_dict['name'],
        "checkin_date": checkin_date,
        "checkout_date": checkout_date,
        "guests": guests,
        "rooms": rooms,
        "user_id": user_id
    }
    
    confirmation_result = generic_confirmation.invoke({
        "message": confirmation_message,
        "operation_details": operation_details
    })
    
    if "拒绝" in confirmation_result or "n" in confirmation_result.lower():
        return f"用户取消了酒店预订操作: {hotel_id}"
    
    # 执行预订逻辑
    booking_id = f"HB{int(datetime.now().timestamp())}"  # 生成预订ID
    
    # 保存检查点
    messages = [f"酒店 {hotel_dict['name']} 预订成功，预订号: {booking_id}"]
    checkpoint_manager.save_checkpoint(thread_id, messages)
    
    cursor.close()
    conn.close()
    
    return f"酒店预订成功，预订号: {booking_id}"


@tool
def cancel_hotel_booking(booking_id: str, config: RunnableConfig) -> str:
    """
    取消酒店预订
    
    Args:
        booking_id: 预订ID
        config: 配置信息
        
    Returns:
        取消结果
    """
    configuration = config.get('configurable', {})
    user_id = configuration.get('user_id', None)
    thread_id = configuration.get('thread_id', 'default_thread')
    if not user_id:
        raise ValueError("User ID is required.")
    
    # 请求用户确认取消操作
    confirmation_message = f"确认取消酒店预订: 取消预订 {booking_id}?"
    operation_details = {
        "booking_id": booking_id,
        "user_id": user_id
    }
    
    confirmation_result = generic_confirmation.invoke({
        "message": confirmation_message,
        "operation_details": operation_details
    })
    
    if "拒绝" in confirmation_result or "n" in confirmation_result.lower():
        return f"用户取消了酒店预订取消操作: {booking_id}"
    
    # 执行取消逻辑
    # 保存检查点
    messages = [f"酒店预订 {booking_id} 已取消"]
    checkpoint_manager.save_checkpoint(thread_id, messages)
    
    return f"酒店预订 {booking_id} 已取消"