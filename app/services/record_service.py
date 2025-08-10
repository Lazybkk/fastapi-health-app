from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import Session

from app.repositories import record_repository
from app.schemas.common import Pagination


class BaseRecordService:
    def __init__(self, repository_module):
        self.repository = repository_module

    def list_records(
        self,
        session: Session,
        user_id: int,
        *,
        limit: int = 10,
        offset: int = 0,
        **filters
    ) -> Pagination:
        records = self.repository.list_records_by_user(
            session, user_id, limit=limit, offset=offset, **filters
        )
        total = self.repository.count_records_by_user(session, user_id, **filters)
        
        return Pagination(
            data=records,
            count=total,
            previous=f"?limit={limit}&offset={max(0, offset - limit)}" if offset > 0 else "",
            next=f"?limit={limit}&offset={offset + limit}" if offset + limit < total else ""
        )

    def create_record(self, session: Session, user_id: int, data: dict):
        return self.repository.create_record(session, user_id=user_id, data=data)

    def get_record(self, session: Session, user_id: int, record_id: int):
        return self.repository.get_record_by_id(session, user_id, record_id)

    def update_record(self, session: Session, user_id: int, record_id: int, data: dict):
        record = self.repository.get_record_by_id(session, user_id, record_id)
        if not record:
            return None
        return self.repository.update_record(session, record, data)

    def delete_record(self, session: Session, user_id: int, record_id: int) -> bool:
        record = self.repository.get_record_by_id(session, user_id, record_id)
        if not record:
            return False
        self.repository.delete_record(session, record)
        return True


class GoalService(BaseRecordService):
    def __init__(self):
        super().__init__(record_repository)

    def list_records(
        self,
        session: Session,
        user_id: int,
        *,
        limit: int = 10,
        offset: int = 0,
        **filters
    ) -> Pagination:
        records = record_repository.list_goals_by_user(
            session, user_id, limit=limit, offset=offset, **filters
        )
        total = record_repository.count_goals_by_user(session, user_id, **filters)
        
        return Pagination(
            data=records,
            count=total,
            previous=f"?limit={limit}&offset={max(0, offset - limit)}" if offset > 0 else "",
            next=f"?limit={limit}&offset={offset + limit}" if offset + limit < total else ""
        )

    def create_record(self, session: Session, user_id: int, data: dict):
        return record_repository.create_goal(session, user_id=user_id, data=data)

    def get_record(self, session: Session, user_id: int, record_id: int):
        return record_repository.get_goal_by_id(session, user_id, record_id)

    def update_record(self, session: Session, user_id: int, record_id: int, data: dict):
        record = record_repository.get_goal_by_id(session, user_id, record_id)
        if not record:
            return None
        return record_repository.update_goal(session, record, data)

    def delete_record(self, session: Session, user_id: int, record_id: int) -> bool:
        record = record_repository.get_goal_by_id(session, user_id, record_id)
        if not record:
            return False
        record_repository.delete_goal(session, record)
        return True


class GoalProgressService(BaseRecordService):
    def __init__(self):
        super().__init__(record_repository)

    def list_records(
        self,
        session: Session,
        goal_id: int,
        *,
        limit: int = 10,
        offset: int = 0,
        **filters
    ) -> Pagination:
        records = record_repository.list_goal_progress_by_goal(
            session, goal_id, limit=limit, offset=offset, **filters
        )
        total = record_repository.count_goal_progress_by_goal(session, goal_id, **filters)
        
        return Pagination(
            data=records,
            count=total,
            previous=f"?limit={limit}&offset={max(0, offset - limit)}" if offset > 0 else "",
            next=f"?limit={limit}&offset={offset + limit}" if offset + limit < total else ""
        )

    def create_record(self, session: Session, goal_id: int, data: dict):
        return record_repository.create_goal_progress(session, goal_id=goal_id, data=data)

    def get_record(self, session: Session, goal_id: int, record_id: int):
        return record_repository.get_goal_progress_by_id(session, goal_id, record_id)

    def update_record(self, session: Session, goal_id: int, record_id: int, data: dict):
        record = record_repository.get_goal_progress_by_id(session, goal_id, record_id)
        if not record:
            return None
        return record_repository.update_goal_progress(session, record, data)

    def delete_record(self, session: Session, goal_id: int, record_id: int) -> bool:
        record = record_repository.get_goal_progress_by_id(session, goal_id, record_id)
        if not record:
            return False
        record_repository.delete_goal_progress(session, record)
        return True


class BodyRecordService(BaseRecordService):
    def __init__(self):
        super().__init__(record_repository)

    def list_records(
        self,
        session: Session,
        user_id: int,
        *,
        limit: int = 10,
        offset: int = 0,
        **filters
    ) -> Pagination:
        records = record_repository.list_body_records_by_user(
            session, user_id, limit=limit, offset=offset, **filters
        )
        total = record_repository.count_body_records_by_user(session, user_id, **filters)
        
        return Pagination(
            data=records,
            count=total,
            previous=f"?limit={limit}&offset={max(0, offset - limit)}" if offset > 0 else "",
            next=f"?limit={limit}&offset={offset + limit}" if offset + limit < total else ""
        )

    def create_record(self, session: Session, user_id: int, data: dict):
        return record_repository.create_body_record(session, user_id=user_id, data=data)

    def get_record(self, session: Session, user_id: int, record_id: int):
        return record_repository.get_body_record_by_id(session, user_id, record_id)

    def update_record(self, session: Session, user_id: int, record_id: int, data: dict):
        record = record_repository.get_body_record_by_id(session, user_id, record_id)
        if not record:
            return None
        return record_repository.update_body_record(session, record, data)

    def delete_record(self, session: Session, user_id: int, record_id: int) -> bool:
        record = record_repository.get_body_record_by_id(session, user_id, record_id)
        if not record:
            return False
        record_repository.delete_body_record(session, record)
        return True


class MealService(BaseRecordService):
    def __init__(self):
        super().__init__(record_repository)

    def list_records(
        self,
        session: Session,
        user_id: int,
        *,
        limit: int = 10,
        offset: int = 0,
        **filters
    ) -> Pagination:
        records = record_repository.list_meals_by_user(
            session, user_id, limit=limit, offset=offset, **filters
        )
        total = record_repository.count_meals_by_user(session, user_id, **filters)
        
        return Pagination(
            data=records,
            count=total,
            previous=f"?limit={limit}&offset={max(0, offset - limit)}" if offset > 0 else "",
            next=f"?limit={limit}&offset={offset + limit}" if offset + limit < total else ""
        )

    def create_record(self, session: Session, user_id: int, data: dict):
        return record_repository.create_meal(session, user_id=user_id, data=data)

    def get_record(self, session: Session, user_id: int, record_id: int):
        return record_repository.get_meal_by_id(session, user_id, record_id)

    def update_record(self, session: Session, user_id: int, record_id: int, data: dict):
        record = record_repository.get_meal_by_id(session, user_id, record_id)
        if not record:
            return None
        return record_repository.update_meal(session, record, data)

    def delete_record(self, session: Session, user_id: int, record_id: int) -> bool:
        record = record_repository.get_meal_by_id(session, user_id, record_id)
        if not record:
            return False
        record_repository.delete_meal(session, record)
        return True


class ExerciseService(BaseRecordService):
    def __init__(self):
        super().__init__(record_repository)

    def list_records(
        self,
        session: Session,
        user_id: int,
        *,
        limit: int = 10,
        offset: int = 0,
        **filters
    ) -> Pagination:
        records = record_repository.list_exercises_by_user(
            session, user_id, limit=limit, offset=offset, **filters
        )
        total = record_repository.count_exercises_by_user(session, user_id, **filters)
        
        return Pagination(
            data=records,
            count=total,
            previous=f"?limit={limit}&offset={max(0, offset - limit)}" if offset > 0 else "",
            next=f"?limit={limit}&offset={offset + limit}" if offset + limit < total else ""
        )

    def create_record(self, session: Session, user_id: int, data: dict):
        return record_repository.create_exercise(session, user_id=user_id, data=data)

    def get_record(self, session: Session, user_id: int, record_id: int):
        return record_repository.get_exercise_by_id(session, user_id, record_id)

    def update_record(self, session: Session, user_id: int, record_id: int, data: dict):
        record = record_repository.get_exercise_by_id(session, user_id, record_id)
        if not record:
            return None
        return record_repository.update_exercise(session, record, data)

    def delete_record(self, session: Session, user_id: int, record_id: int) -> bool:
        record = record_repository.get_exercise_by_id(session, user_id, record_id)
        if not record:
            return False
        record_repository.delete_exercise(session, record)
        return True


class DiaryService(BaseRecordService):
    def __init__(self):
        super().__init__(record_repository)

    def list_records(
        self,
        session: Session,
        user_id: int,
        *,
        limit: int = 10,
        offset: int = 0,
        **filters
    ) -> Pagination:
        records = record_repository.list_diaries_by_user(
            session, user_id, limit=limit, offset=offset, **filters
        )
        total = record_repository.count_diaries_by_user(session, user_id, **filters)
        
        return Pagination(
            data=records,
            count=total,
            previous=f"?limit={limit}&offset={max(0, offset - limit)}" if offset > 0 else "",
            next=f"?limit={limit}&offset={offset + limit}" if offset + limit < total else ""
        )

    def create_record(self, session: Session, user_id: int, data: dict):
        return record_repository.create_diary(session, user_id=user_id, data=data)

    def get_record(self, session: Session, user_id: int, record_id: int):
        return record_repository.get_diary_by_id(session, user_id, record_id)

    def update_record(self, session: Session, user_id: int, record_id: int, data: dict):
        record = record_repository.get_diary_by_id(session, user_id, record_id)
        if not record:
            return None
        return record_repository.update_diary(session, record, data)

    def delete_record(self, session: Session, user_id: int, record_id: int) -> bool:
        record = record_repository.get_diary_by_id(session, user_id, record_id)
        if not record:
            return False
        record_repository.delete_diary(session, record)
        return True


# Service instances
body_record_service = BodyRecordService()
meal_service = MealService()
exercise_service = ExerciseService()
diary_service = DiaryService()
goal_service = GoalService()
goal_progress_service = GoalProgressService()


