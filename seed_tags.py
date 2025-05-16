# seed_tags.py ── 한 번만 실행해 태그/카테고리 넣는 스크립트
from helloSecurity import create_app, db
from helloSecurity.models import Tag, TagCategory

data = {
    "장소":   ["이대", "신촌", "그외"],
    "종류":   ["카페", "식당"],
    "분위기": ["공부하기 좋은", "혼밥하기 좋은", "단체식사하기 좋은",
             "부모님이랑 오기 좋은", "데이트오기 좋은"],
    "음식":   ["일식", "양식", "한식"],
    "가격":   ["가성비", "무난함", "비쌈"],
}

app = create_app()
with app.app_context():
    # 없으면 테이블 생성 (이미 있으면 건너뜀)
    db.create_all()

    for cat_name, tags in data.items():
        # 중복 방지: 같은 이름 카테고리가 있으면 패스
        cat = TagCategory.query.filter_by(name=cat_name).first()
        if not cat:
            cat = TagCategory(name=cat_name)
            db.session.add(cat)
            db.session.flush()        # cat.id 확보

        for t in tags:
            if not Tag.query.filter_by(name=t).first():
                db.session.add(Tag(name=t, category_id=cat.id))

    db.session.commit()
    print("✓ 태그 시드 완료")