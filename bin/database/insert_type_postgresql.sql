INSERT INTO shop_location ( id, name) VALUES()

CREATE TABLE audio_channels ( id, name ) VALUES (1, '2')
CREATE TABLE audio_channels ( id, name ) VALUES (2, '4')
CREATE TABLE audio_channels ( id, name ) VALUES (2, '6')
CREATE TABLE audio_channels ( id, name ) VALUES (2, '8')

CREATE TABLE image_audio_type ( id, name ) VALUES ()

INSERT INTO scale ( id, name ) VALUES (1, '1/1')
INSERT INTO scale ( id, name ) VALUES (2, '1/2')
INSERT INTO scale ( id, name ) VALUES (3, '1/3')
INSERT INTO scale ( id, name ) VALUES (4, '1/4')
INSERT INTO scale ( id, name ) VALUES (5, '1/5')
INSERT INTO scale ( id, name ) VALUES (6, '1/6')
INSERT INTO scale ( id, name ) VALUES (7, '1/7')
INSERT INTO scale ( id, name ) VALUES (8, '1/8')
INSERT INTO scale ( id, name ) VALUES (9, '1/9')
INSERT INTO scale ( id, name ) VALUES (10, '1/10')
INSERT INTO scale ( id, name ) VALUES (11, '1/11')
INSERT INTO scale ( id, name ) VALUES (12, '1/12')
INSERT INTO scale ( id, name ) VALUES (13, '1/50')

INSERT INTO material ( id, name ) VALUES(1, 'PVC')
INSERT INTO material ( id, name ) VALUES(2, 'ABS')
INSERT INTO material ( id, name ) VALUES(3, 'Iron')
INSERT INTO material ( id, name ) VALUES(3, 'Brass')
INSERT INTO material ( id, name ) VALUES(4, 'Silver')
INSERT INTO material ( id, name ) VALUES(5, 'Gold')
INSERT INTO material ( id, name ) VALUES(6, 'Clay')
INSERT INTO material ( id, name ) VALUES(7, 'Nylon')
INSERT INTO material ( id, name ) VALUES(8, 'Silicon')
INSERT INTO material ( id, name ) VALUES(9, 'Aluminium')
INSERT INTO material ( id, name ) VALUES(10, 'Lead')
INSERT INTO material ( id, name ) VALUES(11, 'Magnet')
INSERT INTO material ( id, name ) VALUES(12, 'Acrylic')
INSERT INTO material ( id, name ) VALUES(12, 'Stainless Steel')
INSERT INTO material ( id, name ) VALUES(12, 'Steel')

INSERT INTO audio_codec ( id, name ) VALUES(1, 'AAC', 0)
INSERT INTO audio_codec ( id, name ) VALUES(2, 'AC3', 0)
INSERT INTO audio_codec ( id, name ) VALUES(3, 'ALAC', 1)
INSERT INTO audio_codec ( id, name ) VALUES(4, 'ALS',1)
INSERT INTO audio_codec ( id, name ) VALUES(5, 'AMBE',0)
INSERT INTO audio_codec ( id, name ) VALUES(6, 'AMR',0)
INSERT INTO audio_codec ( id, name ) VALUES(7, 'AMR-WB',0)
INSERT INTO audio_codec ( id, name ) VALUES(8, 'AMR-WB+'0)
INSERT INTO audio_codec ( id, name ) VALUES(9, 'apt-X', 0)
INSERT INTO audio_codec ( id, name ) VALUES(10, 'ATRAC', 1)
INSERT INTO audio_codec ( id, name ) VALUES(11, 'CELT', 0)
INSERT INTO audio_codec ( id, name ) VALUES(12, 'Codec2', 0)
INSERT INTO audio_codec ( id, name ) VALUES(13, 'Enhanced AC3', 0)
INSERT INTO audio_codec ( id, name ) VALUES(14, 'FLAC', 1)
INSERT INTO audio_codec ( id, name ) VALUES(15, 'G.711', 0)
INSERT INTO audio_codec ( id, name ) VALUES(16, 'G.722', 0)
INSERT INTO audio_codec ( id, name ) VALUES(17, 'G.722.1', 0)
INSERT INTO audio_codec ( id, name ) VALUES(18, 'G.722.2', 0)
INSERT INTO audio_codec ( id, name ) VALUES(19, 'G.723.1', 0)
INSERT INTO audio_codec ( id, name ) VALUES(20, 'G.726', 0)
INSERT INTO audio_codec ( id, name ) VALUES(21, 'G.728', 0)
INSERT INTO audio_codec ( id, name ) VALUES(22, 'G.729', 0)
INSERT INTO audio_codec ( id, name ) VALUES(23, 'GSM-FR', 0)
INSERT INTO audio_codec ( id, name ) VALUES(24, 'iLBC', 0)
INSERT INTO audio_codec ( id, name ) VALUES(25, 'iSAC', 0)
INSERT INTO audio_codec ( id, name ) VALUES(26, 'Monkeys Audio', 1)
INSERT INTO audio_codec ( id, name ) VALUES(27, 'MP3', 0)
INSERT INTO audio_codec ( id, name ) VALUES(28, 'MP2', 0)
INSERT INTO audio_codec ( id, name ) VALUES(29, 'Musepack', 0)
INSERT INTO audio_codec ( id, name ) VALUES(30, 'Nellymoser Asao', 0)
INSERT INTO audio_codec ( id, name ) VALUES(31, 'Opus', 0)
INSERT INTO audio_codec ( id, name ) VALUES(32, 'Shorten', 1)
INSERT INTO audio_codec ( id, name ) VALUES(33, 'SILK', 0)
INSERT INTO audio_codec ( id, name ) VALUES(34, 'Siren 7', 0)
INSERT INTO audio_codec ( id, name ) VALUES(35, 'Speex', 0)
INSERT INTO audio_codec ( id, name ) VALUES(36, 'SVOPC', 0)
INSERT INTO audio_codec ( id, name ) VALUES(37, 'TwinVQ', 0)
INSERT INTO audio_codec ( id, name ) VALUES(38, 'Vorbis (Ogg)', 0)
INSERT INTO audio_codec ( id, name ) VALUES(39, 'WavPack', 1)
INSERT INTO audio_codec ( id, name ) VALUES(40, 'TTA', 1)
INSERT INTO audio_codec ( id, name ) VALUES(41, 'Windows Media Audio', 1)

INSERT INTO video_codec ( id, name ) VALUES(1, 'Alpay', 1)
INSERT INTO video_codec ( id, name ) VALUES(2, 'Animation (qtrle)', 1)
INSERT INTO video_codec ( id, name ) VALUES(3, 'ArithYuv', 1)
INSERT INTO video_codec ( id, name ) VALUES(4, 'AVIzlib ', 1)
INSERT INTO video_codec ( id, name ) VALUES(5, 'CamStudio GZIP/LZO ', 1)
INSERT INTO video_codec ( id, name ) VALUES(6, 'Dirac lossless', 1)
INSERT INTO video_codec ( id, name ) VALUES(7, 'FastCodec', 1)
INSERT INTO video_codec ( id, name ) VALUES(8, 'FFV1', 1)
INSERT INTO video_codec ( id, name ) VALUES(9, 'H264 lossless', 1)
INSERT INTO video_codec ( id, name ) VALUES(10, 'Huffyuv', 1)
INSERT INTO video_codec ( id, name ) VALUES(11, 'JPEG 2000 lossless', 1)
INSERT INTO video_codec ( id, name ) VALUES(12, 'Lagarith', 1)
INSERT INTO video_codec ( id, name ) VALUES(13, 'LOCO', 1)
INSERT INTO video_codec ( id, name ) VALUES(14, 'LZO', 1)
INSERT INTO video_codec ( id, name ) VALUES(15, 'MSU Lossless Video Codec', 1)
INSERT INTO video_codec ( id, name ) VALUES(16, 'PNG', 1)
INSERT INTO video_codec ( id, name ) VALUES(17, 'ScreenPressor', 1)
INSERT INTO video_codec ( id, name ) VALUES(18, 'SheerVideo', 1)
INSERT INTO video_codec ( id, name ) VALUES(19, 'Snow lossless', 1)
INSERT INTO video_codec ( id, name ) VALUES(20, 'TechSmith Screen Capture Codec (TSCC)', 1)
INSERT INTO video_codec ( id, name ) VALUES(21, 'Ut Video', 1)
INSERT INTO video_codec ( id, name ) VALUES(22, 'VMNC', 1)
INSERT INTO video_codec ( id, name ) VALUES(23, 'YULS', 1)
INSERT INTO video_codec ( id, name ) VALUES(24, 'ZMBV', 1)
INSERT INTO video_codec ( id, name ) VALUES(25, 'ZRLE', 1)
INSERT INTO video_codec ( id, name ) VALUES(26, 'Blackmagic', 1)
INSERT INTO video_codec ( id, name ) VALUES(27, 'Apple Intermediate Codec', 0)
INSERT INTO video_codec ( id, name ) VALUES(28, 'Audio Video Standard (AVS)', 0)
INSERT INTO video_codec ( id, name ) VALUES(29, 'Bink Video, Smacker video', 0)
INSERT INTO video_codec ( id, name ) VALUES(30, 'Blackbird', 0)
INSERT INTO video_codec ( id, name ) VALUES(31, 'Cinepak', 0)
INSERT INTO video_codec ( id, name ) VALUES(32, 'Dirac', 0)
INSERT INTO video_codec ( id, name ) VALUES(33, 'Firebird', 0)
INSERT INTO video_codec ( id, name ) VALUES(34, 'H.261', 0)
INSERT INTO video_codec ( id, name ) VALUES(35, 'MPEG-1 Part 2', 0)
INSERT INTO video_codec ( id, name ) VALUES(36, 'H.262/MPEG-2 Part 2', 0)
INSERT INTO video_codec ( id, name ) VALUES(37, 'H.263', 0)
INSERT INTO video_codec ( id, name ) VALUES(38, 'Blackmagic', 0)
INSERT INTO video_codec ( id, name ) VALUES(39, 'MPEG-4 Part 2', 0)
INSERT INTO video_codec ( id, name ) VALUES(40, 'H.264/MPEG-4 AVC', 0)
INSERT INTO video_codec ( id, name ) VALUES(41, 'HEVC', 0)
INSERT INTO video_codec ( id, name ) VALUES(42, 'Indeo 3', 0)
INSERT INTO video_codec ( id, name ) VALUES(43, 'Indeo 4', 0)
INSERT INTO video_codec ( id, name ) VALUES(44, 'Indeo 5', 0)
INSERT INTO video_codec ( id, name ) VALUES(45, 'OMS Video', 0)
INSERT INTO video_codec ( id, name ) VALUES(46, 'On2 TrueMotion VP3', 0)
INSERT INTO video_codec ( id, name ) VALUES(47, 'On2 TrueMotion VP4', 0)
INSERT INTO video_codec ( id, name ) VALUES(48, 'On2 TrueMotion VP5', 0)
INSERT INTO video_codec ( id, name ) VALUES(49, 'On2 TrueMotion VP6', 0)
INSERT INTO video_codec ( id, name ) VALUES(50, 'On2 TrueMotion VP7', 0)
INSERT INTO video_codec ( id, name ) VALUES(51, 'On2 TrueMotion VP8', 0)
INSERT INTO video_codec ( id, name ) VALUES(52, 'Pixlet', 0)
INSERT INTO video_codec ( id, name ) VALUES(53, 'RealVideo', 0)
INSERT INTO video_codec ( id, name ) VALUES(54, 'Snow Wavelet Codec', 0)
INSERT INTO video_codec ( id, name ) VALUES(55, 'Sorenson Video', 0)
INSERT INTO video_codec ( id, name ) VALUES(56, 'Sorenson Spark', 0)
INSERT INTO video_codec ( id, name ) VALUES(57, 'Tarkin', 0)
INSERT INTO video_codec ( id, name ) VALUES(58, 'Theora', 0)
INSERT INTO video_codec ( id, name ) VALUES(59, 'VC-1', 0)
INSERT INTO video_codec ( id, name ) VALUES(60, 'VP9', 0)
INSERT INTO video_codec ( id, name ) VALUES(61, 'Windows Media Video', 0)

INSERT INTO ownership_status (
  id
  name 
)
VALUES()

INSERT INTO hash_type (id, name) values (1,'ADLER-32')
INSERT INTO hash_type (id, name) values (2,'CRC-32')
INSERT INTO hash_type (id, name) values (3,'CRC-32B')
INSERT INTO hash_type (id, name) values (4,'CRC-16')
INSERT INTO hash_type (id, name) values (5,'CRC-16-CCITT')
INSERT INTO hash_type (id, name) values (6,'DES(Unix)')
INSERT INTO hash_type (id, name) values (7,'FCS-16')
INSERT INTO hash_type (id, name) values (8,'GHash-32-3')
INSERT INTO hash_type (id, name) values (9,'GHash-32-5')
INSERT INTO hash_type (id, name) values (10,'GOST R 34.11-94')
INSERT INTO hash_type (id, name) values (11,'Haval-160')
INSERT INTO hash_type (id, name) values (12,'Haval-192 110080') 
INSERT INTO hash_type (id, name) values (13,'Haval-224 114080') 
INSERT INTO hash_type (id, name) values (14,'Haval-256')
INSERT INTO hash_type (id, name) values (15,'Lineage II C4')
INSERT INTO hash_type (id, name) values (16,'Domain Cached Credentials')
INSERT INTO hash_type (id, name) values (17,'XOR-32')
INSERT INTO hash_type (id, name) values (18,'Haval-128')
INSERT INTO hash_type (id, name) values (19,'MD2')
INSERT INTO hash_type (id, name) values (20,'MD4')
INSERT INTO hash_type (id, name) values (21,'MD5')
INSERT INTO hash_type (id, name) values (22,'NTLM')
INSERT INTO hash_type (id, name) values (23,'RAdmin v2.x')
INSERT INTO hash_type (id, name) values (24,'RipeMD-128')
INSERT INTO hash_type (id, name) values (25,'RipeMD-160')
INSERT INTO hash_type (id, name) values (26,'RipeMD-256')
INSERT INTO hash_type (id, name) values (27,'RipeMD-320')
INSERT INTO hash_type (id, name) values (28,'SNEFRU-128')
INSERT INTO hash_type (id, name) values (29,'SNEFRU-256')
INSERT INTO hash_type (id, name) values (30,'SAM')
INSERT INTO hash_type (id, name) values (31,'SHA-1')
INSERT INTO hash_type (id, name) values (32,'SHA-224')
INSERT INTO hash_type (id, name) values (33,'SHA-384')
INSERT INTO hash_type (id, name) values (34,'SHA-256')
INSERT INTO hash_type (id, name) values (35,'SHA-512')
INSERT INTO hash_type (id, name) values (36,'Tiger-128')
INSERT INTO hash_type (id, name) values (37,'Tiger-160')
INSERT INTO hash_type (id, name) values (38,'Tiger-192')
INSERT INTO hash_type (id, name) values (39,'Whirlpool')

INSERT INTO release_edition_read_status_type (
  id
  name 
)
VALUES()

INSERT INTO release_type ( id, name ) VALUES(1, 'Mod')
INSERT INTO release_type ( id, name ) VALUES(2, 'Game')
INSERT INTO release_type ( id, name ) VALUES(3, 'Chapter')
INSERT INTO release_type ( id, name ) VALUES(4, 'Volume')
INSERT INTO release_type ( id, name ) VALUES(5, 'Episode')


INSERT INTO software_type (
  id
  name 
)
VALUES()
INSERT INTO edition_type (
  id
  name 
)
VALUES()
INSERT INTO image_entity_edition_type (
  id
  name 
)
VALUES()

INSERT INTO image_company_type (id, name) VALUES(1, 'Logo')
INSERT INTO image_company_type (id, name) VALUES(2, 'Front')
INSERT INTO image_company_type (id, name) VALUES(3, 'Back')
INSERT INTO image_company_type (id, name) VALUES(4, 'Above')
INSERT INTO image_company_type (id, name) VALUES(5, 'Within')
INSERT INTO image_company_type (id, name) VALUES(6, 'Google Map')



INSERT INTO image_goods_type (
  id
  name 
)
VALUES()
INSERT INTO create_type (
  id
  name 
)
VALUES()
INSERT INTO produces_type (
  id
  name 
)
VALUES()
INSERT INTO product_condition_type (
  id
  name 
)
VALUES()
INSERT INTO figure_version (
  id
  name 
)
VALUES()
INSERT INTO plataform_type (
  id
  name 
)
VALUES()
INSERT INTO print_type (
  id
  name 
)
VALUES()
INSERT INTO related_type (
  id
  name 
)
VALUES()
INSERT INTO release_ownership_type (
  id
  name 
)
VALUES()
INSERT INTO entity_type (
  id
  name 
)
VALUES()
INSERT INTO filter_type (
  id
  name 
)
VALUES()
INSERT INTO user_filter_type (
  id
  name 
)
VALUES()
INSERT INTO edition_read_status_type (
  id
  name 
)
VALUES()
INSERT INTO function_type (
  id
  name 
)
VALUES()
INSERT INTO condition_type (
  id
  name 
)
VALUES()
INSERT INTO classification_type ( id, name ) VALUES(1, 'Free')
INSERT INTO classification_type ( id, name ) VALUES(2, '3+')
INSERT INTO classification_type ( id, name ) VALUES(3, '4+')
INSERT INTO classification_type ( id, name ) VALUES(4, '5+')
INSERT INTO classification_type ( id, name ) VALUES(5, '6+')
INSERT INTO classification_type ( id, name ) VALUES(6, '7+')
INSERT INTO classification_type ( id, name ) VALUES(7, '8+')
INSERT INTO classification_type ( id, name ) VALUES(8, '9+')
INSERT INTO classification_type ( id, name ) VALUES(9, '10+')
INSERT INTO classification_type ( id, name ) VALUES(10, '11+')
INSERT INTO classification_type ( id, name ) VALUES(11, '12+')
INSERT INTO classification_type ( id, name ) VALUES(12, '13+')
INSERT INTO classification_type ( id, name ) VALUES(13, '14+')
INSERT INTO classification_type ( id, name ) VALUES(14, '15+')
INSERT INTO classification_type ( id, name ) VALUES(15, '16+')
INSERT INTO classification_type ( id, name ) VALUES(16, '17+')
INSERT INTO classification_type ( id, name ) VALUES(17, '18+')

INSERT INTO collaborator_type (
  id
  name 
);

INSERT INTO media_type ( id, name ) VALUES(1,'Disk Floppy')
INSERT INTO media_type ( id, name ) VALUES(2,'CD')
INSERT INTO media_type ( id, name ) VALUES(3,'DVD')
INSERT INTO media_type ( id, name ) VALUES(4,'DAT TAPE')
INSERT INTO media_type ( id, name ) VALUES(5,'HD-DVD')
INSERT INTO media_type ( id, name ) VALUES(6,'BluRay')

INSERT INTO media_type ( id, name ) VALUES(7,'HDTV')
INSERT INTO media_type ( id, name ) VALUES(8,'SDTV')
INSERT INTO media_type ( id, name ) VALUES(9,'PDTV')

/* Volume oneshot must have Oneshot on number field */
INSERT INTO number_type ( id, name) VALUES(1,'Volume')
INSERT INTO number_type ( id, name) VALUES(2,'Chapter')
INSERT INTO number_type ( id, name) VALUES(2,'Edition')
INSERT INTO number_type ( id, name) VALUES(2,'Season')
INSERT INTO number_type ( id, name) VALUES(2,'Episode')

INSERT INTO alias_type ( id, name ) VALUES(1, 'Main')
INSERT INTO alias_type ( id, name ) VALUES(2, 'Alias')
INSERT INTO alias_type ( id, name ) VALUES(3, 'Nickname')
INSERT INTO alias_type ( id, name ) VALUES(4, 'Title')
INSERT INTO alias_type ( id, name ) VALUES(5, 'Subtitle')
INSERT INTO alias_type ( id, name ) VALUES(6, 'Romanized Title')
INSERT INTO alias_type ( id, name ) VALUES(7, 'Romanized Subtitle')


INSERT INTO mod_type (
  id
  name 
)
VALUES()
INSERT INTO blood_type (
  id
  name 
);
INSERT INTO box_condition_type (
  id
  name 
)
VALUES()
INSERT INTO based_type (
  id
  name 
)
VALUES()
INSERT INTO stage_developer_type (
  id
  name 
)
VALUES()
INSERT INTO company_function_type (
  id
  name 
)
VALUES()
INSERT INTO soundtrack_type (
  id
  name 
)
VALUES()
INSERT INTO compose_type (
  id
  name 
) 
VALUES()
INSERT INTO image_soundtrack_type (
  id
  name 
)
VALUES()

INSERT INTO image_user_type ( id, name ) VALUES( 1, 'profile')

INSERT INTO lyric_type (
  id
  name 
)
VALUES()
INSERT INTO social_type (
  id
  name 
  website 
  website_secure 
)
VALUES()
INSERT INTO country (
  id
  name 
  code 
)
VALUES()
INSERT INTO language (
  id
  name 
  code 
)
VALUES()
INSERT INTO image (
  id 
  url 
  extension 
  name 
)
VALUES()
INSERT INTO shops (
  id
  url 
  name 
)
VALUES()
INSERT INTO currency (
  id
  name 
  symbol 
  code 
)
VALUES()
INSERT INTO collaborator (
  id
  name 
  irc 
  description 
  create_date
)
VALUES()
INSERT INTO collaborator_member (
  id
  name 
  active
)
VALUES()
INSERT INTO users (
  id
  username 
  pass 
  gender
  location 
  birthday
  signup_date
  activated
)
VALUES()
INSERT INTO spider_item (
  id
  identify 
  url 
  complete_crawled
)
VALUES()
INSERT INTO tag (
  id
  name 
)
VALUES()
INSERT INTO category (
  id
  name 
)
VALUES()
INSERT INTO genre (
  id
  name 
)
VALUES()
INSERT INTO collection (
  id
  name 
  description 
)
VALUES()
INSERT INTO lists_goods (
  id
  user_id
  name 
  create_date
);
INSERT INTO user_email (
  users_id
  email 
)
VALUES()
INSERT INTO company (
  id
  country_id
  name 
  social_name 
  start_year 
  foundation_date
  website 
  description 
  create_date
)
VALUES()
INSERT INTO collaborator_website (
  collaborator_id
  website 
)
VALUES()
INSERT INTO soundtrack (
  id
  soundtrack_type_id
  name 
  launch_year 
)
VALUES()
INSERT INTO social (
  id
  social_type_id
  url 
)
VALUES()
INSERT INTO event (
  id
  name 
  edition 
  location 
  website 
  date
  duration
  free
)
VALUES()
INSERT INTO version (
  id
  stage_developer_type_id
  number 
  changelog 
)
VALUES()
INSERT INTO requirements (
  id
  version_id
  video_board 
  processor 
  memory 
  hd_storage 
)
VALUES()
INSERT INTO user_filter (
  id
  user_filter_type_id
  users_id
  name 
)
VALUES()
INSERT INTO people (
  id 
  country_id
  blood_type_id
  website 
  description 
)
VALUES()
INSERT INTO users_has_social (
  users_id
  social_id
  last_checked
  create_date
)
VALUES()
INSERT INTO tag_has_filter_type (
  filter_type_id
  tag_id
)
VALUES()
INSERT INTO people_has_social (
  social_id
  people_id 
  last_checked
  create_date
)
VALUES()
INSERT INTO collaborator_has_social (
  social_id
  collaborator_id
  create_date
  last_checked
)
VALUES()
INSERT INTO shops_operate_on_country (
  shops_id
  country_id
)
VALUES()
INSERT INTO people_nacionalization_on_country (
  people_id 
  country_id
);
INSERT INTO country_has_language (
  language_id
  country_id
)
VALUES()
INSERT INTO collaborator_has_collaborator_member (
  collaborator_id
  collaborator_member_id
  founder
);
INSERT INTO soundtrack_integrate_collection (
  collection_id
  soundtrack_id
)
VALUES()
INSERT INTO category_has_filter_type (
  category_id
  filter_type_id
)
VALUES()
INSERT INTO genre_has_filter_type (
  genre_id
  filter_type_id
)
VALUES()
INSERT INTO audio (
  id
  country_id
  audio_codec_id
  name 
  duration TIME NULL,
  bitrate
)
VALUES()
INSERT INTO audio_has_language (
  audio_id
  language_id
)
VALUES()
INSERT INTO company_sponsors_event (
  company_id
  event_id
)
VALUES()
INSERT INTO country_has_currency (
  currency_id
  country_id
  main
)
VALUES()
INSERT INTO company_owner_collection (
  company_id
  collection_id
)
VALUES()
INSERT INTO company_has_country (
  country_id
  company_id
)
VALUES()
INSERT INTO company_has_social (
  social_id
  company_id
  last_checked
  create_date
)
VALUES()
INSERT INTO people_has_image (
  image_id 
  people_id 
)
VALUES()
INSERT INTO lists_edition (
  id
  entity_type_id
  user_id
  name 
  create_date
)
VALUES()
INSERT INTO lists_release (
  id
  entity_type_id
  user_id
  name 
  create_date
)
VALUES()
INSERT INTO audio_has_genre (
  genre_id
  audio_id
)
VALUES()
INSERT INTO soundtrack_has_image (
  soundtrack_id
  image_id 
  image_soundtrack_type_id
)
VALUES()
INSERT INTO lyrics (
  id
  lyric_type_id
  user_id
  audio_id
  language_id
  title 
  lyric 
)
VALUES()
INSERT INTO entity (
  id 
  entity_type_id
  classification_type_id
  collection_id
  language_id
  country_id
  launch_year 
  collection_started
)
VALUES()
INSERT INTO driver (
  id
  requirements_id
  name 
  url_download 
)
VALUES()
INSERT INTO entity_description (
  language_id
  entity_id 
  description 
)
VALUES()
INSERT INTO entity_wiki (
  id
  language_id
  entity_id 
  name 
  url 
)
VALUES()
INSERT INTO archive (
  id 
  version_id
  name 
  url 
  size
  extension 
)
VALUES()
INSERT INTO entity_synopse (
  entity_id 
  language_id
  content 
)
VALUES()
INSERT INTO people_alias(
  id
  alias_type_id
  people_id 
  name 
  lastname 
)
VALUES()
INSERT INTO persona (
  id
  blood_type_id
  entity_id 
  name 
  gender SET NULL,
  birthday
  first_appear_on 
  height
  weight DECIMAL NULL,
  eyes_color 
  hair_color 
)
VALUES()
INSERT INTO soundtrack_has_audio (
  soundtrack_id
  audio_id
  exclusive
);
INSERT INTO entity_has_category (
  entity_id 
  category_id
)
VALUES()
INSERT INTO entity_has_tag (
  tag_id
  entity_id 
)
VALUES()
INSERT INTO hash (
  id 
  hash_type_id
  archive_id 
  code 
  create_date
)
VALUES()
INSERT INTO persona_related_persona (
  persona_id
  another_persona_id
  related_type_id
)
VALUES()
INSERT INTO entity_based_entity (
  entity_id 
  another_entity_id
  based_type_id
)
VALUES()
INSERT INTO entity_alias (
  id
  people_alias_type_id
  entity_id 
  language_id
  name 
)
VALUES()
INSERT INTO entity_edition (
  id
  edition_type_id
  event_id
  entity_id 
  title 
  free
  release_description 
  censored
  code 
  complement_code 
  height
  width
  depth
  weight DECIMAL NULL,
);
INSERT INTO entity_release (
  id 
  entity_id 
  release_type_id
  country_id
  entity_edition_id
  description 
  release_date
)
VALUES()
INSERT INTO software_edition (
  entity_edition_id
  plataform_type_id
  software_type_id
  media_type_id
)
VALUES()
INSERT INTO people_compose_audio (
  audio_id
  people_id 
  people_alias_id
  compose_type_id
)
VALUES()
INSERT INTO people_produces_entity (
  people_id 
  entity_id 
  people_alias_id
  produces_type_id
)
VALUES()
INSERT INTO goods (
  id 
  entity_id 
  goods_version_id
  currency_id
  scale_id
  country_id
  height TINYINT UNSIGNED NOT NULL,
  width TINYINT UNSIGNED NULL,
  weight DECIMAL NULL,
  launch_price DECIMAL NOT NULL,
  release_date
  observation 
)
VALUES()
INSERT INTO lists_edition_list_entity_edition (
  lists_edition_id
  entity_edition_id
  ownership_status_id
  condition_type_id
  edition_read_status_type_id
  observation 
)
VALUES()
INSERT INTO lists_goods_list_goods (
  lists_goods_id
  goods_id 
  ownership_status_id
  box_condition_type_id
  product_condition_type_id
  observation 
)
VALUES()
INSERT INTO persona_unusual_features (
  id
  persona_id
  name 
)
VALUES()
INSERT INTO persona_alias (
  id
  persona_id
  name,
  type_id
)
VALUES()
INSERT INTO persona_occupation (
  id
  persona_id
  occupation 
)
VALUES()
INSERT INTO game_release (
  entity_release_id 
  emulate
  installation_instructions 
)
VALUES()
INSERT INTO persona_affiliation (
  id
  persona_id
  name 
)
VALUES()
INSERT INTO persona_race (
  id
  persona_id
  name 
)
VALUES()
INSERT INTO software_edition_has_version (
  software_edition_id
  version_id
)
VALUES()
INSERT INTO read_edition (
  entity_edition_id
  print_type_id
  pages_number
  chapters_number
);
INSERT INTO software_edition_has_subtitle (
  software_edition_id
  subtitle_id
)
VALUES()
INSERT INTO soundtrack_for_entity_edition (
  soundtrack_id
  entity_edition_id
)
VALUES()
INSERT INTO entity_edition_launch_country (
  entity_edition_id
  country_id
  launch_date
  launch_price DECIMAL NOT NULL,
)
VALUES()
INSERT INTO entity_edition_has_subtitle (
  subtitle_id
  entity_edition_id
)
VALUES()
INSERT INTO entity_edition_has_language (
  entity_edition_id
  language_id
)
VALUES()
INSERT INTO entity_edition_has_currency (
  entity_edition_id
  currency_id
)
VALUES()
INSERT INTO goods_from_persona (
  goods_id 
  persona_id
)
VALUES()
INSERT INTO goods_has_category (
  category_id
  goods_id 
)
VALUES()
INSERT INTO entity_release_has_version (
  entity_release_id 
  version_id
)
VALUES()
INSERT INTO entity_release_has_language (
  entity_release_id 
  language_id
)
VALUES()
INSERT INTO goods_has_material (
  goods_id 
  material_id
)
VALUES()
INSERT INTO mod (
  id
  entity_release_id 
  mod_type_id
  name 
  author 
  launch_date
  description 
  installation_instruction 
)
VALUES()
INSERT INTO goods_has_shop_location (
  goods_id 
  shop_location_id
)
VALUES()
INSERT INTO goods_has_tag (
  tag_id
  goods_id 
)
VALUES()
INSERT INTO goods_has_shops (
  goods_id 
  shops_id
  product_url 
  checked_last
)
VALUES()
INSERT INTO mod_has_image (
  mod_id
  image_id 
)
VALUES()
INSERT INTO collaborator_provides_release (
  collaborator_id
  entity_release_id 
  collaborator_type_id
)
VALUES()
INSERT INTO collaborator_member_produces_entity_release (
  collaborator_member_id
  entity_release_id 
  collaborator_member_type_id
)
VALUES()

CREATE TABLE archive_container (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
);


CREATE TABLE url_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
);

INSERT INTO entity_edition_has_company (
  company_id
  entity_edition_id
  company_function_type_id
)
VALUES()
INSERT INTO entity_has_company (
  company_id
  entity_id 
  company_function_type_id
)
VALUES()
INSERT INTO goods_has_image (
  image_id 
  goods_id 
  image_goods_type_id
)
VALUES()
INSERT INTO entity_edition_has_image (
  image_id 
  entity_edition_id
  image_entity_edition_type_id
)
VALUES()
INSERT INTO number_edition (
  id
  entity_edition_id
  number_type_id
  entity_type_id
  number
);
INSERT INTO number_release (
  id
  number_release_id
  entity_release_id 
  number_type_id
  entity_type_id
  number
)
VALUES()
INSERT INTO lists_release_list_entity_release (
  lists_release_id
  entity_release_id 
  release_edition_read_status_type_id
  release_ownership_type_id
  local_storage 
)
VALUES()
INSERT INTO people_produces_goods (
  people_id 
  goods_id 
  people_alias_id
  create_type_id
)
VALUES()
INSERT INTO soundtrack_comments (
  id
  soundtrack_id
  users_id
  content 
  title 
  create_date
  update_date
)
VALUES()
INSERT INTO audio_comments (
  id
  audio_id
  users_id
  content 
  title 
  create_date
  update_date
)
VALUES()
INSERT INTO company_comments (
  id
  company_id
  users_id
  content 
  title 
  create_date
  update_date
)
VALUES()
INSERT INTO people_comments (
  id
  people_id 
  users_id
  content 
  title 
  create_date
  update_date
)
VALUES()
INSERT INTO goods_comments (
  id
  goods_id 
  users_id
  content 
  title 
  create_date
  update_date
)
VALUES()
INSERT INTO entity_edition_comments (
  id
  entity_edition_id
  users_id
  content 
  title 
  create_date
  update_date
)
VALUES()
INSERT INTO entity_release_comments (
  id
  entity_release_id 
  users_id
  content 
  title 
  create_date
  update_date
)
VALUES()
INSERT INTO people_voice_persona (
  persona_id
  people_id 
  language_id
  entity_id 
  entity_edition_id
  observation 
);
INSERT INTO tag_user_filter (
  user_filter_id
  tag_id
)
VALUES()
INSERT INTO classification_user_filter (
  user_filter_id
  classification_id
)
VALUES()
INSERT INTO category_user_filter (  user_filter_id
  category_id
) VALUES