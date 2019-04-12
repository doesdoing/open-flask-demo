Example:
    import sqlite3_plus

    1.search SQL:
        test=sqlite3_plus.sqlite3_plus(path='./xxx.db',Tab='xxx').find(ip='xxx')
    2.add SQL:
        sqlite3_plus.sqlite3_plus(path='./xxx.db',Tab='xxx').add(Data={"a":"xxx","b":"xxx"})
    3.update SQL:
        sqlite3_plus.sqlite3_plus(path='./xxx.db',Tab='xxx').update(Data={"a":"xxx","b":"xxx"} , ID='xxxx')
    4.delete SQL:
        sqlite3_plus.sqlite3_plus(ath='./xxx.db',Tab='xxx')..delete(ID=['xx','xx'])