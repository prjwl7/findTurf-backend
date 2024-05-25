from models import db, Jersey
from sqlalchemy.exc import SQLAlchemyError

def create_jersey(data):
    try:
        new_jersey = Jersey(
            name=data['name'],
            team=data['team'],
            league=data['league'],
            type=data['type'],
            home_away_third=data['home_away_third'],
            sizes=','.join(data['sizes']),  # Convert list to comma-separated string
            number_of_jerseys=data['number_of_jerseys'],
            price=data['price'],
            customizable=data['customizable'],
            discounted_price=data['discounted_price'],
            image_url=data['image_url']
        )
        db.session.add(new_jersey)
        db.session.commit()
        return new_jersey
    except SQLAlchemyError as e:
        db.session.rollback()
        raise ValueError(f"Database error: {str(e)}")

def get_jerseys(search='', sort_by='', home_away_third='', team='', price=''):
    try:
        query = Jersey.query

        if search:
            query = query.filter(
                (Jersey.name.ilike(f'%{search}%')) |
                (Jersey.team.ilike(f'%{search}%'))
            )

        if home_away_third:
            query = query.filter_by(home_away_third=home_away_third)

        if team:
            query = query.filter_by(team=team)

        if price:
            if price == 'Under 500':
                query = query.filter(Jersey.price < 500)
            elif price == '500-1000':
                query = query.filter(Jersey.price.between(500, 1000))
            elif price == 'Above 1000':
                query = query.filter(Jersey.price > 1000)

        if sort_by:
            if sort_by == 'Low-High':
                query = query.order_by(Jersey.price.asc())
            elif sort_by == 'High-Low':
                query = query.order_by(Jersey.price.desc())
            elif sort_by == 'A-Z':
                query = query.order_by(Jersey.name.asc())
            elif sort_by == 'Z-A':
                query = query.order_by(Jersey.name.desc())
        
        return query.all()
    except SQLAlchemyError as e:
        raise ValueError(f"Database error: {str(e)}")

def update_jersey(jersey_id, data):
    try:
        jersey = Jersey.query.get(jersey_id)
        if not jersey:
            raise ValueError("Jersey not found")

        jersey.name = data.get('name', jersey.name)
        jersey.team = data.get('team', jersey.team)
        jersey.league = data.get('league', jersey.league)
        jersey.type = data.get('type', jersey.type)
        jersey.home_away_third = data.get('home_away_third', jersey.home_away_third)
        jersey.sizes = ','.join(data.get('sizes', jersey.sizes.split(',')))
        jersey.number_of_jerseys = data.get('number_of_jerseys', jersey.number_of_jerseys)
        jersey.price = data.get('price', jersey.price)
        jersey.customizable = data.get('customizable', jersey.customizable)
        jersey.discounted_price = data.get('discounted_price', jersey.discounted_price)
        jersey.image_url = data.get('image_url', jersey.image_url)

        db.session.commit()
        return jersey
    except SQLAlchemyError as e:
        db.session.rollback()
        raise ValueError(f"Database error: {str(e)}")

def delete_jersey(jersey_id):
    try:
        jersey = Jersey.query.get(jersey_id)
        if not jersey:
            raise ValueError("Jersey not found")

        db.session.delete(jersey)
        db.session.commit()
        return jersey
    except SQLAlchemyError as e:
        db.session.rollback()
        raise ValueError(f"Database error: {str(e)}")
