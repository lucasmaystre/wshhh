INSERT INTO user (id, email, pw_hash) VALUES (1, 'bengiuliano@gmail.com', 'pbkdf2:sha1:1000$SlPdbA6v$418988fb52845995862db8af55625cd5add12085');

INSERT INTO item (id, user_id, created) VALUES (1, 1, "2016-11-19 13:23:37.052");
INSERT INTO item (id, user_id, created) VALUES (2, 1, "2016-11-20 03:09:56.172");
INSERT INTO item (id, user_id, created) VALUES (3, 1, "2016-11-20 04:47:04.837");
INSERT INTO item (id, user_id, created) VALUES (4, 1, "2016-11-20 05:09:42.642");
INSERT INTO item (id, user_id, created) VALUES (5, 1, "2016-11-20 05:12:42.642");
INSERT INTO item (id, user_id, created) VALUES (6, 1, "2016-11-20 05:15:42.642");
INSERT INTO item (id, user_id, created) VALUES (7, 1, "2016-11-20 05:21:42.642");

INSERT INTO itemattribute (item_id, attribute_id) VALUES (1, 5);
INSERT INTO itemattribute (item_id, attribute_id) VALUES (1, 9);
INSERT INTO itemattribute (item_id, attribute_id) VALUES (1, 15);
INSERT INTO itemattribute (item_id, attribute_id) VALUES (1, 16);

INSERT INTO itemattribute (item_id, attribute_id) VALUES (2, 1);
INSERT INTO itemattribute (item_id, attribute_id) VALUES (2, 7);
INSERT INTO itemattribute (item_id, attribute_id) VALUES (2, 29);

INSERT INTO itemattribute (item_id, attribute_id) VALUES (3, 24);
INSERT INTO itemattribute (item_id, attribute_id) VALUES (3, 39);
INSERT INTO itemattribute (item_id, attribute_id) VALUES (3, 4);

INSERT INTO itemattribute (item_id, attribute_id) VALUES (4, 19);
INSERT INTO itemattribute (item_id, attribute_id) VALUES (4, 2);

INSERT INTO itemattribute (item_id, attribute_id) VALUES (5, 3);
INSERT INTO itemattribute (item_id, attribute_id) VALUES (5, 17);

INSERT INTO itemattribute (item_id, attribute_id) VALUES (6, 35);
INSERT INTO itemattribute (item_id, attribute_id) VALUES (6, 25);

INSERT INTO itemattribute (item_id, attribute_id) VALUES (7, 8);
INSERT INTO itemattribute (item_id, attribute_id) VALUES (7, 33);

INSERT INTO image (item_id, thumbnail_filename, fullres_filename) VALUES (1, 'thumb_1.jpg', 'full_1.jpg');
INSERT INTO image (item_id, thumbnail_filename, fullres_filename) VALUES (2, 'thumb_2.jpg', 'full_2.jpg');
INSERT INTO image (item_id, thumbnail_filename, fullres_filename) VALUES (3, 'thumb_3.jpg', 'full_3.jpg');
INSERT INTO image (item_id, thumbnail_filename, fullres_filename) VALUES (4, 'thumb_5.jpg', 'full_5.jpg');
INSERT INTO image (item_id, thumbnail_filename, fullres_filename) VALUES (5, 'thumb_7.jpg', 'full_7.jpg');
INSERT INTO image (item_id, thumbnail_filename, fullres_filename) VALUES (6, 'thumb_8.jpg', 'full_8.jpg');
INSERT INTO image (item_id, thumbnail_filename, fullres_filename) VALUES (7, 'thumb_10.jpg', 'full_10.jpg');
