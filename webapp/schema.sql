CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    email TEXT,
    pw_hash TEXT
);
CREATE INDEX user_email_idx ON user(email);

CREATE TABLE item (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES user,
    created TIMESTAMP
);
CREATE INDEX item_user_id_idx ON item(user_id);

CREATE TABLE attribute (
    id INTEGER PRIMARY KEY,
    filename TEXT,
    description TEXT
);

CREATE TABLE itemattribute (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES item,
    attribute_id INTEGER REFERENCES attribute
);
CREATE INDEX itemattribute_item_id_idx ON itemattribute(item_id);
CREATE INDEX itemattribute_attribute_id_idx ON itemattribute(attribute_id);

CREATE TABLE image (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES item,
    thumbnail_filename TEXT,
    fullres_filename TEXT
);
CREATE INDEX image_item_id_idx ON image(item_id);
