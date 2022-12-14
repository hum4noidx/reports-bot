import datetime
from typing import List


class Repo:
    """Db abstraction layer"""

    def __init__(self, conn):
        self.conn = conn

    # users
    async def add_user(self, user_id: int, full_name: str) -> None:
        await self.conn.execute(
            'INSERT INTO users(tg_id, full_name) VALUES($1,$2) '
            'ON CONFLICT(tg_id) DO NOTHING', user_id, full_name)
        return

    async def list_users(self) -> List[int]:
        """List all bot users"""
        ids = await self.conn.fetch(
            'SELECT user_id from users'
        )
        data = ([uid['user_id'] for uid in ids])
        return data

    async def get_admins(self) -> List[int]:
        admins = await self.conn.fetch(
            'SELECT user_id FROM users WHERE admin = True'
        )
        data = ([admin['user_id'] for admin in admins])
        return data

    async def get_user(self, tg_id):
        result = await self.conn.fetch('SELECT tg_id, full_name, custom_id, schedule, real_name FROM users WHERE tg_id = $1',
                                       tg_id)
        return result

    async def get_user_schedule(self, tg_id):
        return await self.conn.execute('SELECT schedule FROM users WHERE tg_id = $1', tg_id)

    async def update_schedule(self, tg_id: int, schedule: str):
        return await self.conn.execute('UPDATE users SET schedule = $2 WHERE tg_id = $1', tg_id, schedule)

    async def save_report_file(self, user_id: int, file_id: str, report_date, comment: str = None):
        return await self.conn.execute('INSERT INTO user_reports (user_id, file_id, report_date, comment) '
                                       'VALUES ($1,$2,$3,$4) ON CONFLICT ON CONSTRAINT unique_report '
                                       'DO UPDATE SET file_id = $2',
                                       user_id, file_id, report_date, comment)

    async def get_today_reports(self, date=datetime.date.today()):
        result = await self.conn.fetch('SELECT users.real_name, file_id, comment, user_id '
                                       'FROM user_reports '
                                       'LEFT JOIN users on user_reports.user_id = users.tg_id '
                                       'WHERE report_date=$1', date)
        return result

    async def user_save_name(self, user_id, real_name):
        return await self.conn.execute('UPDATE users SET real_name = $1 WHERE tg_id = $2', real_name, user_id)
