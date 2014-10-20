begin transaction;
    pragma foreign_keys = on;
    create table Shows(
        show_id integer primary key autoincrement,
        show_name text,
        unique(show_name)
    );
    create table Aliases(
        alias_id integer primary key autoincrement,
        show_id integer,
        alias_name text,
        foreign key(show_id) references Shows(show_id) on delete cascade,
        unique(alias_name)
    );
commit;
