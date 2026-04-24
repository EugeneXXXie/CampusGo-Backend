from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.activity import Activity
from app.models.activity_comment import ActivityComment
from app.core.security import get_password_hash
from app.models.activity_category import ActivityCategory
from app.models.user import User

CATEGORIES = ["羽毛球", "篮球", "自习", "桌游", "探店", "摄影", "骑行", "音乐"]


def seed_initial_data(session: Session) -> None:
    for index, name in enumerate(CATEGORIES, start=1):
        existed = session.scalar(select(ActivityCategory).where(ActivityCategory.name == name))
        if existed is None:
            session.add(ActivityCategory(name=name, sort=index))

    demo_user = session.scalar(select(User).where(User.phone == "18800001111"))
    if demo_user is None:
        session.add(
            User(
                phone="18800001111",
                password_hash=get_password_hash("123456"),
                nickname="林小跃",
                avatar="",
                college="信息工程学院",
                grade="大三",
                bio="周末球局、自习搭子、摄影扫街都能约。",
            )
        )
        session.commit()
        demo_user = session.scalar(select(User).where(User.phone == "18800001111"))

    assert demo_user is not None

    category_map = {
        item.name: item
        for item in session.scalars(select(ActivityCategory)).all()
    }

    demo_activities = [
        {
            "title": "南操夜跑搭子局",
            "category": "骑行",
            "description": "晚饭后 6 公里轻松跑，配速友好，新手也能跟上。集合后先热身，结束后一起喝冰豆浆。",
            "activity_time": datetime.now() + timedelta(days=2, hours=2),
            "location": "南操场北门",
            "max_participants": 8,
            "current_participants": 5,
            "audit_required": False,
            "status": "open",
            "contact_info": "微信：campusgo-run",
            "comments": [
                "我平时 6 分半配速，可以一起吗？",
                "女生友好吗？",
            ],
        },
        {
            "title": "图书馆四楼期中自习搭子",
            "category": "自习",
            "description": "计划从下午两点到五点，番茄钟模式自习，适合需要有人陪着进入状态的同学。",
            "activity_time": datetime.now() + timedelta(days=3, hours=1),
            "location": "图书馆四楼东区",
            "max_participants": 6,
            "current_participants": 4,
            "audit_required": True,
            "status": "open",
            "contact_info": "QQ：1254001",
            "comments": [
                "会不会太吵？",
            ],
        },
        {
            "title": "周末羽毛球混双上分",
            "category": "羽毛球",
            "description": "体育馆 3 号场地，强度中等，来 3 到 5 个人轮换打，想找能长期约球的人。",
            "activity_time": datetime.now() + timedelta(days=4, hours=4),
            "location": "校体育馆羽毛球馆",
            "max_participants": 6,
            "current_participants": 6,
            "audit_required": False,
            "status": "full",
            "contact_info": "微信：fly-smash",
            "comments": [
                "周末下午我能到，缺搭档吗？",
            ],
        },
        {
            "title": "傍晚校园扫街摄影互拍",
            "category": "摄影",
            "description": "欢迎手机党和相机党，趁日落前走一圈教学楼和湖边，互拍人像和环境照。",
            "activity_time": datetime.now() + timedelta(days=5, hours=3),
            "location": "行政楼台阶集合",
            "max_participants": 10,
            "current_participants": 3,
            "audit_required": False,
            "status": "open",
            "contact_info": "微信：frames-on-campus",
            "comments": [
                "可以带朋友一起来吗？",
            ],
        },
    ]

    for item in demo_activities:
        existed = session.scalar(select(Activity).where(Activity.title == item["title"]))
        if existed is not None:
            continue

        category = category_map.get(str(item["category"]))
        if category is None:
            continue

        activity = Activity(
            user_id=demo_user.id,
            category_id=category.id,
            title=str(item["title"]),
            cover="",
            description=str(item["description"]),
            activity_time=item["activity_time"],
            location=str(item["location"]),
            max_participants=int(item["max_participants"]),
            current_participants=int(item["current_participants"]),
            audit_required=bool(item["audit_required"]),
            status=str(item["status"]),
            contact_info=str(item["contact_info"]),
            view_count=0,
        )
        session.add(activity)
        session.flush()

        for index, content in enumerate(item["comments"], start=1):
            session.add(
                ActivityComment(
                    activity_id=activity.id,
                    user_id=demo_user.id,
                    parent_id=None,
                    content=str(content),
                )
            )

    session.commit()
