import src.database_operations as db

def get_2_random():
    cat1 = db.get_random_cat()
    cat2 = db.get_random_cat()
    while cat2[0] == cat1[0]:  # Ensure different cats using IDs
        cat2 = db.get_random_cat()
    return [(cat1[0], cat1[1]), (cat2[0], cat2[1])]