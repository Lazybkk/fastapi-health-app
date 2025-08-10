from __future__ import annotations

import random
from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.core.security import get_password_hash
from app.models import (
    User,
    Article,
    Tag,
    ArticleTag,
    BodyRecord,
    Meal,
    Exercise,
    Diary,
    Goal,
    GoalProgress,
)


def get_or_create_user(session: Session, email: str, name: str, password: str) -> User:
    user = session.scalars(select(User).where(User.email == email)).first()
    if user:
        return user
    user = User(email=email, name=name, password_hash=get_password_hash(password))
    session.add(user)
    session.flush()
    return user


def get_or_create_tag(session: Session, name: str) -> Tag:
    tag = session.scalars(select(Tag).where(Tag.name == name)).first()
    if tag:
        return tag
    tag = Tag(name=name)
    session.add(tag)
    session.flush()
    return tag


def get_or_create_article(session: Session, title: str, category: str, image_url: str | None) -> Article:
    art = session.scalars(select(Article).where(Article.title == title)).first()
    if art:
        return art
    art = Article(title=title, content=f"Sample content for {title}", image_url=image_url, category=category)
    session.add(art)
    session.flush()
    return art


def ensure_article_tag(session: Session, article_id: int, tag_id: int) -> None:
    exists = session.scalars(
        select(ArticleTag).where(ArticleTag.article_id == article_id, ArticleTag.tag_id == tag_id)
    ).first()
    if not exists:
        session.add(ArticleTag(article_id=article_id, tag_id=tag_id))


def seed_articles(session: Session) -> None:
    categories = ["Recommended", "Diet", "Beauty", "Health"]
    tag_names = ["low-carb", "fitness", "sleep", "skin", "mental", "yoga", "keto", "cardio"]
    tags = [get_or_create_tag(session, n) for n in tag_names]

    for i in range(1, 13):
        category = random.choice(categories)
        title = f"Article {i}: {category} insights"
        image_url = f"https://picsum.photos/seed/{i}/400/300"
        art = get_or_create_article(session, title=title, category=category, image_url=image_url)
        assigned = random.sample(tags, k=random.randint(1, 3))
        for t in assigned:
            ensure_article_tag(session, art.id, t.id)


def seed_goals(session: Session, user: User) -> None:
    """Seed demo goals for the user"""
    goal_data = [
        {
            "title": "Lose 5kg",
            "description": "Target weight loss goal",
            "target_value": 65.0,
            "target_date": date.today() + timedelta(days=30),
        },
        {
            "title": "Exercise 3 times per week",
            "description": "Regular exercise routine",
            "target_value": 3.0,
            "target_date": date.today() + timedelta(days=7),
        },
        {
            "title": "Reduce body fat to 18%",
            "description": "Body composition goal",
            "target_value": 18.0,
            "target_date": date.today() + timedelta(days=60),
        },
        {
            "title": "Eat healthy meals daily",
            "description": "Nutrition goal",
            "target_value": 7.0,
            "target_date": date.today() + timedelta(days=7),
        },
    ]
    
    goals = []
    for goal_info in goal_data:
        goal = Goal(
            user_id=user.id,
            **goal_info
        )
        session.add(goal)
        session.flush()
        goals.append(goal)
    
    # Add some progress for goals
    today = date.today()
    for goal in goals:
        # Add progress for the last 7 days
        for d in range(7):
            progress_date = today - timedelta(days=d)
            
            # Randomly complete some goals
            is_completed = random.random() < 0.6  # 60% completion rate
            
            progress = GoalProgress(
                goal_id=goal.id,
                date=progress_date,
                current_value=random.uniform(goal.target_value * 0.3, goal.target_value * 0.9),
                is_completed=is_completed,
                notes=f"Progress update for {progress_date.isoformat()}"
            )
            session.add(progress)


def seed_records(session: Session, user: User) -> None:
    today = date.today()
    base_weight = 70.0
    base_fat = 20.0
    meal_types = ["Morning", "Lunch", "Dinner", "Snack"]

    for d in range(14):
        day = today - timedelta(days=d)

        # Body record
        if not session.scalars(select(BodyRecord).where(BodyRecord.user_id == user.id, BodyRecord.date == day)).first():
            session.add(
                BodyRecord(
                    user_id=user.id,
                    date=day,
                    weight=round(base_weight + random.uniform(-1.5, 1.5), 1),
                    body_fat_percentage=round(base_fat + random.uniform(-1.0, 1.0), 1),
                )
            )

        # Meals (2-3/day)
        todays_meals = random.sample(meal_types, k=random.randint(2, 3))
        for mt in todays_meals:
            session.add(
                Meal(
                    user_id=user.id,
                    date=day,
                    meal_type=mt,
                    image_url="https://picsum.photos/seed/meal{}/200/150".format(random.randint(1, 9999)),
                    description=f"{mt} meal",
                    calories=random.randint(150, 700),
                )
            )

        # Exercise (50% days)
        if random.random() < 0.5:
            session.add(
                Exercise(
                    user_id=user.id,
                    date=day,
                    name=random.choice(["Run", "Swim", "Cycling", "Yoga"]),
                    duration_min=random.randint(20, 60),
                    calories=random.randint(100, 500),
                )
            )

        # Diary (50% days)
        if random.random() < 0.5:
            session.add(
                Diary(
                    user_id=user.id,
                    date=day,
                    time=None,
                    content=f"Diary entry for {day.isoformat()}",
                )
            )


def main() -> None:
    session: Session = SessionLocal()
    try:
        user = get_or_create_user(session, email="demo@example.com", name="Demo User", password="demo1234")
        seed_articles(session)
        seed_goals(session, user)
        seed_records(session, user)
        session.commit()
        print("Seed completed. User email=demo@example.com, password=demo1234")
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()


