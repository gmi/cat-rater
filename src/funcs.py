import src.database_operations as db

def get_2_random():
    cat1 = db.get_random_cat()
    cat2 = db.get_random_cat()
    while cat2 == cat1:
        print("woah, 1 in 10k chance of 2 same cats")
        cat2 == db.get_random_cat()
    return [cat1[1], cat2[1]]

