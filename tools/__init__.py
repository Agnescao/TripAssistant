#得到项目的路径
from pathlib import Path

basic_dir = Path(__file__).resolve().parent.parent

db=f"{basic_dir}/travel_agent.db"

local_file = f"{basic_dir}/travel_agent.db"

#创建一个backup db 方便测试
backup_file = f"{basic_dir}/travel_agent_backup.db"