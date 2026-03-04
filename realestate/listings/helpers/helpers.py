from django.db.models import Q

def order_by(order):
    if (order == "noviji"): return "-created_at"
    if order == "skuplji": return "-price"
    if order == "jeftiniji": return "price"
    if order == "veći": return "-area"
    if order == "manji": return "area"
    return "-created_at"

def where_city(city):
    # 2 Parametrized queries
    return Q(city=city) if city else Q()

def where_room_count(room_count):
    # 2 Parametrized queries
    return Q(room_count=room_count) if room_count else Q()

def where_price(price_from, price_to):
    # 2 Parametrized queries
    if price_from and price_to: return Q(price__range=(price_from, price_to))
    elif price_from: return Q(price__gte=price_from)
    elif price_to: return Q(price__lte=price_to)
    return Q()

def where_area(m2_from, m2_to):
    # 2 Parametrized queries
    if m2_from and m2_to: return Q(area__range=(m2_from, m2_to))
    elif m2_from: return Q(area__gte=m2_from)
    elif m2_to: return Q(area__lte=m2_to)
    return Q()

def where(data):
    query = Q()
    query &= where_city(data["grad"])
    query &= where_room_count(data["broj_soba"])
    query &= where_price(data["cena_od"], data["cena_do"])
    query &= where_area(data["m2_do"], data["m2_do"])
    return query