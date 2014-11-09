CREATE TYPE gender AS ENUM ('Female', 'Male', 'Undefined');

/* This is not a table_type */
CREATE TABLE IF NOT EXISTS shop_location (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS scale (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS taste_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS material (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS audio_codec (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  lossless BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS video_codec (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  lossless BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS ownership_status (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

/* Begin table types */

CREATE TABLE IF NOT EXISTS hash_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS chinese_sign (
	id SERIAL,
	name VARCHAR NOT NULL,
	PRIMARY KEY(id)
);
CREATE TABLE IF NOT EXISTS zodiac_sign (
	id SERIAL,
	name VARCHAR NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS release_edition_read_status_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS release_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS software_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;


CREATE TABLE IF NOT EXISTS image_audio_type (
  id SERIAL,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS edition_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS image_entity_edition_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS image_goods_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS create_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS produces_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS product_condition_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS figure_version (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS plataform_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS print_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS related_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS release_ownership_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS entity_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS filter_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS user_filter_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS edition_read_status_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS function_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS condition_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS classification_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS collaborator_type (
  id SERIAL,
  name VARCHAR UNIQUE NULL,
  PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS media_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS number_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS archive_container (
  id SERIAL,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS alias_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS mod_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS blood_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS blood_rh_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS box_condition_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS based_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS stage_developer_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS company_function_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS soundtrack_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS compose_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
) 
;

CREATE TABLE IF NOT EXISTS image_soundtrack_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS image_user_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS visual_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS image_collaborator_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS image_company_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS lyric_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS goods_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS favorite_type (
	id SERIAL,
	name VARCHAR UNIQUE NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS weapon_type (
	id SERIAL,
	name VARCHAR UNIQUE NOT NULL,
	PRIMARY KEY(id)
);

/* Not the same structure as table_type */

CREATE TABLE IF NOT EXISTS social_type (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  website VARCHAR NOT NULL,
  website_secure VARCHAR NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS url_type (
  id SERIAL,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS audio_channels (
  id SERIAL,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
;


/* country and language */

CREATE TABLE IF NOT EXISTS country (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  code VARCHAR UNIQUE NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS language (
  id SERIAL,
  name VARCHAR NOT NULL,
  code VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

/* Images */

CREATE TABLE IF NOT EXISTS image (
  id BIGSERIAL,
  url VARCHAR NOT NULL,
  extension VARCHAR NOT NULL,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS shops (
  id SERIAL,
  url VARCHAR UNIQUE NULL,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
;

/* Currency */

/* Update database */ 
CREATE TABLE IF NOT EXISTS currency (
  id SERIAL,
  name VARCHAR NOT NULL,
  symbol VARCHAR NULL,
  code VARCHAR UNIQUE NOT NULL,
  number VARCHAR(3) UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS collaborator (
  id SERIAL,
  country_id INTEGER  NOT NULL,
  name VARCHAR NOT NULL,
  irc VARCHAR NULL,
  description TEXT NULL,
  foundation_date DATE NOT NULL DEFAULT now(),
  create_date timestamp without time zone NOT NULL DEFAULT now(),
  UNIQUE(country_id, name),
  PRIMARY KEY(id),
  FOREIGN KEY(country_id)
    REFERENCES country(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
  
)
;

CREATE TABLE IF NOT EXISTS collaborator_member (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  active BOOLEAN NOT NULL DEFAULT TRUE,
  PRIMARY KEY(id)
)
;


CREATE TABLE IF NOT EXISTS users (
  id SERIAL,
  username VARCHAR UNIQUE NOT NULL,
  pass VARCHAR NOT NULL,
  gender gender NOT NULL,
  location VARCHAR NULL,
  birthday DATE NOT NULL,
  signup_date timestamp without time zone NOT NULL DEFAULT now(),
  activated BOOLEAN NOT NULL DEFAULT TRUE,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS spider_item (
  id BIGINT NOT NULL,
  table_name VARCHAR NOT NULL,
  url VARCHAR NOT NULL,
  complete_crawled BOOLEAN NOT NULL DEFAULT False
);

CREATE TABLE IF NOT EXISTS tag (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS category (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS genre (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS collection (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  description TEXT NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS lists_goods (
  id SERIAL,
  user_id INTEGER  NOT NULL,
  name VARCHAR NULL,
  create_date timestamp without time zone NOT NULL DEFAULT now(),
  PRIMARY KEY(id),
  FOREIGN KEY(user_id)
    REFERENCES users(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS user_email (
  user_id INTEGER  NOT NULL,
  email VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(user_id, email),
  FOREIGN KEY(user_id)
    REFERENCES users(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
)
;

/* change table on postgreSQL contry_id to null*/
CREATE TABLE IF NOT EXISTS company (
  id SERIAL,
  country_id INTEGER NULL,
  name VARCHAR NOT NULL,
  social_name VARCHAR NULL,
  start_year CHAR(4) NULL,
  foundation_date DATE NULL,
  website VARCHAR NULL,
  description TEXT NULL,
  create_date timestamp without time zone NOT NULL DEFAULT now(),
  PRIMARY KEY(id),
  FOREIGN KEY(country_id)
    REFERENCES country(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS collaborator_website (
  collaborator_id INTEGER  NOT NULL,
  website VARCHAR NOT NULL,
  PRIMARY KEY(collaborator_id, website),
  FOREIGN KEY(collaborator_id)
    REFERENCES collaborator(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS soundtrack (
  id SERIAL,
  country_id INTEGER  NOT NULL,
  soundtrack_type_id INTEGER  NOT NULL,
  name VARCHAR NOT NULL,
  launch_year CHAR(4) NOT NULL,
  code VARCHAR NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(soundtrack_type_id)
    REFERENCES soundtrack_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(country_id)
    REFERENCES country(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS social (
  id SERIAL,
  social_type_id INTEGER  NOT NULL,
  url VARCHAR NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(social_type_id)
    REFERENCES social_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS event (
  id SERIAL,
  name VARCHAR NOT NULL,
  edition VARCHAR NOT NULL,
  location VARCHAR NULL,
  website VARCHAR NULL,
  country_id INTEGER  NOT NULL,
  date DATE NOT NULL,
  duration INTEGER  NULL,
  free BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY(id),
  FOREIGN KEY(country_id)
    REFERENCES country(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS version (
  id SERIAL,
  stage_developer_type_id INTEGER  NOT NULL,
  number VARCHAR NOT NULL,
  changelog TEXT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(stage_developer_type_id)
    REFERENCES stage_developer_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS requirements (
  id SERIAL,
  version_id INTEGER  NOT NULL,
  video_board VARCHAR NOT NULL,
  processor VARCHAR NOT NULL,
  memory VARCHAR NOT NULL,
  hd_storage VARCHAR NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(version_id)
    REFERENCES version(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS user_filter (
  id SERIAL,
  user_filter_type_id INTEGER  NOT NULL,
  user_id INTEGER  NOT NULL,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(user_id)
    REFERENCES users(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(user_filter_type_id)
    REFERENCES user_filter_type(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS people (
  id BIGSERIAL,
  country_id INTEGER  NOT NULL,
  blood_type_id INTEGER  NULL,
  blood_rh_type_id INTEGER  NULL,
  gender gender NULL,
  website VARCHAR NULL,
  description TEXT NULL,
  birth_place VARCHAR NULL,
  birth_date VARCHAR NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(blood_type_id)
    REFERENCES blood_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(country_id)
    REFERENCES country(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
FOREIGN KEY(blood_rh_type_id)
    REFERENCES blood_rh_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS users_has_social (
  user_id INTEGER  NOT NULL,
  social_id INTEGER  NOT NULL,
  last_checked timestamp without time zone NOT NULL DEFAULT now(),
  create_date timestamp without time zone NOT NULL DEFAULT now(),
  PRIMARY KEY(user_id, social_id),
  FOREIGN KEY(user_id)
    REFERENCES users(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(social_id)
    REFERENCES social(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS tag_has_filter_type (
  filter_type_id INTEGER  NOT NULL,
  tag_id INTEGER  NOT NULL,
  PRIMARY KEY(filter_type_id, tag_id),
  FOREIGN KEY(filter_type_id)
    REFERENCES filter_type(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(tag_id)
    REFERENCES tag(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS people_has_social (
  social_id INTEGER  NOT NULL,
  people_id BIGINT  NOT NULL,
  last_checked timestamp without time zone NOT NULL DEFAULT now(),
  create_date timestamp without time zone NOT NULL DEFAULT now(),
  PRIMARY KEY(social_id, people_id),
  FOREIGN KEY(social_id)
    REFERENCES social(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(people_id)
    REFERENCES people(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS collaborator_has_social (
  social_id INTEGER  NOT NULL,
  collaborator_id INTEGER  NOT NULL,
  last_checked timestamp without time zone NOT NULL DEFAULT now(),
  create_date timestamp without time zone NOT NULL DEFAULT now(),
  PRIMARY KEY(social_id, collaborator_id),
  FOREIGN KEY(social_id)
    REFERENCES social(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(collaborator_id)
    REFERENCES collaborator(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS shops_operate_on_country (
  shops_id INTEGER  NOT NULL,
  country_id INTEGER  NOT NULL,
  PRIMARY KEY(shops_id, country_id),
  FOREIGN KEY(shops_id)
    REFERENCES shops(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(country_id)
    REFERENCES country(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS people_nacionalization_on_country (
  people_id BIGINT  NOT NULL,
  country_id INTEGER  NOT NULL,
  PRIMARY KEY(people_id, country_id),
  FOREIGN KEY(people_id)
    REFERENCES people(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(country_id)
    REFERENCES country(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS country_has_language (
  language_id INTEGER  NOT NULL,
  country_id INTEGER  NOT NULL,
  PRIMARY KEY(language_id, country_id),
  FOREIGN KEY(language_id)
    REFERENCES language(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(country_id)
    REFERENCES country(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS collaborator_has_collaborator_member (
  collaborator_id INTEGER  NOT NULL,
  collaborator_member_id INTEGER  NOT NULL,
  founder BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY(collaborator_id, collaborator_member_id),
  FOREIGN KEY(collaborator_id)
    REFERENCES collaborator(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(collaborator_member_id)
    REFERENCES collaborator_member(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS soundtrack_integrate_collection (
  collection_id INTEGER  NULL,
  soundtrack_id INTEGER  NOT NULL,
  PRIMARY KEY(collection_id, soundtrack_id),
  FOREIGN KEY(collection_id)
    REFERENCES collection(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(soundtrack_id)
    REFERENCES soundtrack(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS category_has_filter_type (
  category_id INTEGER  NOT NULL,
  filter_type_id INTEGER  NOT NULL,
  PRIMARY KEY(category_id, filter_type_id),
  FOREIGN KEY(category_id)
    REFERENCES category(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(filter_type_id)
    REFERENCES filter_type(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS genre_has_filter_type (
  genre_id INTEGER  NOT NULL,
  filter_type_id INTEGER  NOT NULL,
  PRIMARY KEY(genre_id, filter_type_id),
  FOREIGN KEY(genre_id)
    REFERENCES category(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(filter_type_id)
    REFERENCES filter_type(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS audio (
  id SERIAL,
  audio_channels_id INTEGER  NOT NULL,
  country_id INTEGER  NOT NULL,
  audio_codec_id INTEGER  NOT NULL,
  name VARCHAR NOT NULL,
  duration TIME NULL,
  bitrate INTEGER  NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(audio_codec_id)
    REFERENCES audio_codec(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(country_id)
    REFERENCES country(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(audio_channels_id)
    REFERENCES audio_channels(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS audio_has_language (
  audio_id INTEGER  NOT NULL,
  language_id INTEGER  NOT NULL,
  PRIMARY KEY(audio_id, language_id),
  FOREIGN KEY(audio_id)
    REFERENCES audio(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(language_id)
    REFERENCES language(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS company_sponsors_event (
  company_id INTEGER  NOT NULL,
  event_id INTEGER  NOT NULL,
  PRIMARY KEY(company_id, event_id),
  FOREIGN KEY(company_id)
    REFERENCES company(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(event_id)
    REFERENCES event(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS country_has_currency (
  currency_id INTEGER  NOT NULL,
  country_id INTEGER  NOT NULL,
  main BOOLEAN NOT NULL DEFAULT TRUE,
  PRIMARY KEY(currency_id, country_id),
  FOREIGN KEY(currency_id)
    REFERENCES currency(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(country_id)
    REFERENCES country(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS company_owner_collection (
  company_id INTEGER  NOT NULL,
  collection_id INTEGER  NOT NULL,
  PRIMARY KEY(company_id, collection_id),
  FOREIGN KEY(company_id)
    REFERENCES company(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(collection_id)
    REFERENCES collection(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS company_has_country (
  country_id INTEGER  NOT NULL,
  company_id INTEGER  NOT NULL,
  PRIMARY KEY(country_id, company_id),
  FOREIGN KEY(country_id)
    REFERENCES country(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(company_id)
    REFERENCES company(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS company_has_social (
  social_id INTEGER  NOT NULL,
  company_id INTEGER  NOT NULL,
  last_checked timestamp without time zone NOT NULL DEFAULT now(),
  create_date timestamp without time zone NOT NULL DEFAULT now(),
  PRIMARY KEY(social_id, company_id),
  FOREIGN KEY(social_id)
    REFERENCES social(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(company_id)
    REFERENCES company(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS people_has_image (
  image_id BIGINT  NOT NULL,
  people_id BIGINT  NOT NULL,
  PRIMARY KEY(image_id, people_id),
  FOREIGN KEY(image_id)
    REFERENCES image(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(people_id)
    REFERENCES people(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS lists_edition (
  id SERIAL,
  entity_type_id INTEGER  NOT NULL,
  user_id INTEGER  NOT NULL,
  name VARCHAR NOT NULL,
  create_date timestamp without time zone NOT NULL DEFAULT now(),
  PRIMARY KEY(id),
  FOREIGN KEY(user_id)
    REFERENCES users(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_type_id)
    REFERENCES entity_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS lists_release (
  id SERIAL,
  entity_type_id INTEGER  NOT NULL,
  user_id INTEGER  NOT NULL,
  name VARCHAR NOT NULL,
  create_date timestamp without time zone NOT NULL DEFAULT now(),
  PRIMARY KEY(id),
  FOREIGN KEY(user_id)
    REFERENCES users(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_type_id)
    REFERENCES entity_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS audio_has_genre (
  genre_id INTEGER  NOT NULL,
  audio_id INTEGER  NOT NULL,
  PRIMARY KEY(genre_id, audio_id),
  FOREIGN KEY(genre_id)
    REFERENCES genre(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(audio_id)
    REFERENCES audio(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS soundtrack_has_image (
  soundtrack_id INTEGER  NOT NULL,
  image_id BIGINT NOT NULL,
  image_soundtrack_type_id INTEGER  NOT NULL,
  PRIMARY KEY(soundtrack_id, image_id),
  FOREIGN KEY(soundtrack_id)
    REFERENCES soundtrack(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(image_id)
    REFERENCES image(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(image_soundtrack_type_id)
    REFERENCES image_soundtrack_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS lyric (
  id SERIAL,
  lyric_type_id INTEGER  NOT NULL,
  user_id INTEGER  NULL,
  audio_id INTEGER  NOT NULL,
  language_id INTEGER  NOT NULL,
  title VARCHAR NOT NULL,
  lyric TEXT NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(language_id)
    REFERENCES language(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(audio_id)
    REFERENCES audio(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(user_id)
    REFERENCES users(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(lyric_type_id)
    REFERENCES lyric_type(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS entity (
  id BIGSERIAL,
  entity_type_id INTEGER  NOT NULL,
  classification_type_id INTEGER  NOT NULL,
  collection_id INTEGER NULL,
  language_id INTEGER  NOT NULL,
  country_id INTEGER  NOT NULL,
  launch_year VARCHAR NULL,
  collection_started BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY(id),
  FOREIGN KEY(country_id)
    REFERENCES country(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(language_id)
    REFERENCES language(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(collection_id)
    REFERENCES collection(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(classification_type_id)
    REFERENCES classification_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_type_id)
    REFERENCES entity_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS driver (
  id SERIAL,
  name VARCHAR UNIQUE NOT NULL,
  url_download VARCHAR NULL,
  PRIMARY KEY(id)
)
;

CREATE TABLE IF NOT EXISTS entity_description (
  id SERIAL,
  language_id INTEGER  NOT NULL,
  entity_id BIGINT  NOT NULL,
  description TEXT NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(entity_id)
    REFERENCES entity(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(language_id)
    REFERENCES language(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS goods (
  id BIGSERIAL,
  collection_id INTEGER  NULL,
  goods_type_id INTEGER  NOT NULL,
  height SMALLINT  NOT NULL,
  width SMALLINT  NULL,
  weight DECIMAL NULL,
  observation TEXT NULL,
  has_counterfeit BOOL NOT NULL,
  collection_started BOOL NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(goods_type_id)
    REFERENCES goods_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(collection_id)
    REFERENCES collection(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS entity_wiki (
  id SERIAL,
  language_id INTEGER  NOT NULL,
  entity_id BIGINT  NOT NULL,
  name VARCHAR NOT NULL,
  url VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id, language_id),
  FOREIGN KEY(entity_id)
    REFERENCES entity(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(language_id)
    REFERENCES language(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS archive (
  id BIGSERIAL,
  version_id INTEGER  NOT NULL,
  name VARCHAR NOT NULL,
  size INTEGER  NOT NULL,
  extension VARCHAR NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(version_id)
    REFERENCES version(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS entity_synopsis (
  entity_id BIGINT  NOT NULL,
  language_id INTEGER  NOT NULL,
  content TEXT NOT NULL,
  PRIMARY KEY(entity_id, language_id),
  FOREIGN KEY(entity_id)
    REFERENCES entity(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(language_id)
    REFERENCES language(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS people_alias (
  id SERIAL,
  alias_type_id INTEGER  NOT NULL,
  people_id BIGINT  NOT NULL,
  name VARCHAR NOT NULL,
  lastname VARCHAR NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(people_id)
    REFERENCES people(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(alias_type_id)
    REFERENCES alias_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS persona (
  id SERIAL,
  blood_type_id INTEGER NULL,
  blood_rh_type_id INTEGER NULL,
  gender gender NOT NULL,
  birthday VARCHAR NULL,
  birthyear VARCHAR NULL,
  age VARCHAR NULL,
  apparent_age VARCHAR NULL,
  height DECIMAL NULL,
  weight DECIMAL NULL,
  eyes_color VARCHAR NULL,
  hair_color VARCHAR NULL,
  hair_lenght VARCHAR NULL,
  exact_hair_color VARCHAR NULL,
  bust_size VARCHAR NULL,
  waist_size VARCHAR NULL,
  butt_size VARCHAR NULL,
  chinese_sign_id INTEGER NULL,
  zodiac_sign_id INTEGER NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(blood_type_id)
    REFERENCES blood_type(id)
      ON DELETE SET NULL
      ON UPDATE CASCADE,
  FOREIGN KEY(blood_rh_type_id)
    REFERENCES blood_rh_type(id)
      ON DELETE SET NULL
      ON UPDATE CASCADE,
  FOREIGN KEY(chinese_sign_id)
    REFERENCES chinese_sign(id)
      ON DELETE SET NULL
      ON UPDATE CASCADE,
 FOREIGN KEY(zodiac_sign_id)
    REFERENCES zodiac_sign(id)
      ON DELETE SET NULL
      ON UPDATE CASCADE,
)
;



CREATE TABLE IF NOT EXISTS persona_element (
	id SERIAL,
	name VARCHAR NOT NULL,
	persona_id INTEGER NOT NULL,
	PRIMARY KEY(id),
	FOREIGN KEY(persona_id)
    REFERENCES persona(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS persona_weakness (
	id SERIAL,
	name VARCHAR NOT NULL,
	persona_id INTEGER NOT NULL,
	PRIMARY KEY(id),
	FOREIGN KEY(persona_id)
    REFERENCES persona(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS persona_power (
	id SERIAL,
	name VARCHAR NOT NULL,
	persona_id INTEGER NOT NULL,
	PRIMARY KEY(id),
	FOREIGN KEY(persona_id)
    REFERENCES persona(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);




CREATE TABLE IF NOT EXISTS persona_taste (
	id SERIAL,
	name VARCHAR NOT NULL,
	persona_id INTEGER NOT NULL,
	taste_type_id INTEGER NOT NULL,
	PRIMARY KEY(id),
	FOREIGN KEY(persona_id)
    REFERENCES persona(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
	FOREIGN KEY(taste_type_id)
    REFERENCES taste_type(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS persona_favorite (
	id SERIAL,
	name VARCHAR NOT NULL,
	persona_id INTEGER NOT NULL,
	favorite_type_id INTEGER NOT NULL,
	PRIMARY KEY(id),
	FOREIGN KEY(persona_id)
    REFERENCES persona(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
	FOREIGN KEY(favorite_type_id)
    REFERENCES favorite_type(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS persona_weapon (
	id SERIAL,
	name VARCHAR NOT NULL,
	persona_id INTEGER NOT NULL,
	weapon_type_id INTEGER NOT NULL,
	PRIMARY KEY(id),
	FOREIGN KEY(persona_id)
    REFERENCES persona(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
	FOREIGN KEY(weapon_type_id)
    REFERENCES weapon_type(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);


CREATE TABLE IF NOT EXISTS soundtrack_has_audio (
  soundtrack_id INTEGER  NOT NULL,
  audio_id INTEGER  NOT NULL,
  exclusive BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY(soundtrack_id, audio_id),
  FOREIGN KEY(soundtrack_id)
    REFERENCES soundtrack(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(audio_id)
    REFERENCES audio(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS entity_has_category (
  entity_id BIGINT  NOT NULL,
  category_id INTEGER  NOT NULL,
  PRIMARY KEY(entity_id, category_id),
  FOREIGN KEY(entity_id)
    REFERENCES entity(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(category_id)
    REFERENCES category(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS entity_has_tag (
  tag_id INTEGER  NOT NULL,
  entity_id BIGINT  NOT NULL,
  PRIMARY KEY(tag_id, entity_id),
  FOREIGN KEY(tag_id)
    REFERENCES tag(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_id)
    REFERENCES entity(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS entity_has_genre (
  genre_id INTEGER  NOT NULL,
  entity_id BIGINT  NOT NULL,
  PRIMARY KEY(genre_id, entity_id),
  FOREIGN KEY(genre_id)
    REFERENCES genre(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_id)
    REFERENCES entity(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS hash (
  id BIGSERIAL,
  hash_type_id INTEGER  NOT NULL,
  archive_id BIGINT  NOT NULL,
  code TEXT NOT NULL,
  create_date timestamp without time zone NOT NULL DEFAULT now(),
  PRIMARY KEY(id),
  FOREIGN KEY(archive_id)
    REFERENCES archive(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(hash_type_id)
    REFERENCES hash_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS persona_related_persona (
  persona_id INTEGER NOT NULL,
  another_persona_id INTEGER  NOT NULL,
  related_type_id INTEGER  NOT NULL,
  PRIMARY KEY(persona_id, another_persona_id, related_type_id),
  FOREIGN KEY(persona_id)
    REFERENCES persona(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(another_persona_id)
    REFERENCES persona(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(related_type_id)
    REFERENCES related_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS entity_based_entity (
  entity_id BIGINT  NOT NULL,
  another_entity_id INTEGER  NOT NULL,
  based_type_id INTEGER  NOT NULL,
  PRIMARY KEY(entity_id, another_entity_id, based_type_id),
  FOREIGN KEY(entity_id)
    REFERENCES entity(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(another_entity_id)
    REFERENCES entity(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(based_type_id)
    REFERENCES based_type(id)
      ON DELETE SET DEFAULT
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS entity_alias (
  id SERIAL,
  alias_type_id INTEGER  NOT NULL,
  entity_id BIGINT  NOT NULL,
  language_id INTEGER  NOT NULL,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(language_id)
    REFERENCES language(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_id)
    REFERENCES entity(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(alias_type_id)
    REFERENCES alias_type(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;



CREATE TABLE IF NOT EXISTS entity_edition (
  id SERIAL,
  edition_type_id INTEGER  NOT NULL,
  event_id INTEGER  NULL,
  entity_id BIGINT  NOT NULL,
  title VARCHAR NOT NULL,
  subtitle VARCHAR NULL,
  free BOOLEAN NOT NULL DEFAULT FALSE,
  release_description TEXT NULL,
  censored BOOLEAN NOT NULL DEFAULT FALSE,
  code VARCHAR NULL,
  complement_code VARCHAR NULL,
  height INTEGER  NULL,
  width INTEGER  NULL,
  depth INTEGER  NULL,
  weight DECIMAL NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(entity_id)
    REFERENCES entity(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(event_id)
    REFERENCES event(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(edition_type_id)
    REFERENCES edition_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS entity_release (
  id BIGSERIAL,
  entity_id BIGINT  NOT NULL,
  release_type_id INTEGER  NOT NULL,
  country_id INTEGER  NOT NULL,
  entity_edition_id INTEGER NULL,
  description TEXT NULL,
  release_date timestamp without time zone NOT NULL DEFAULT now(),
  PRIMARY KEY(id),
  FOREIGN KEY(entity_edition_id)
    REFERENCES entity_edition(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(country_id)
    REFERENCES country(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(release_type_id)
    REFERENCES release_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_id)
    REFERENCES entity(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS software_edition (
  entity_edition_id INTEGER  NOT NULL,
  plataform_type_id INTEGER  NOT NULL,
  software_type_id INTEGER  NOT NULL,
  media_type_id INTEGER  NOT NULL,
  visual_type_id INTEGER  NOT NULL,
  PRIMARY KEY(entity_edition_id),
  FOREIGN KEY(entity_edition_id)
    REFERENCES entity_edition(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(media_type_id)
    REFERENCES media_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(software_type_id)
    REFERENCES software_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(plataform_type_id)
    REFERENCES plataform_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(visual_type_id)
    REFERENCES visual_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS people_compose_audio (
  audio_id INTEGER  NOT NULL,
  people_id BIGINT  NOT NULL,
  people_alias_id INTEGER  NOT NULL,
  compose_type_id INTEGER  NOT NULL,
  PRIMARY KEY(audio_id, people_id, compose_type_id),
  FOREIGN KEY(audio_id)
    REFERENCES audio(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(people_id)
    REFERENCES people(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(compose_type_id)
    REFERENCES compose_type(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(people_alias_id)
    REFERENCES people_alias(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS people_produces_entity (
  people_id BIGINT  NOT NULL,
  entity_id BIGINT  NOT NULL,
  people_alias_id INTEGER  NOT NULL,
  produces_type_id INTEGER  NOT NULL,
  PRIMARY KEY(people_id, entity_id, produces_type_id),
  FOREIGN KEY(people_id)
    REFERENCES people(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_id)
    REFERENCES entity(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(produces_type_id)
    REFERENCES produces_type(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(people_alias_id)
    REFERENCES people_alias(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS lists_edition_list_entity_edition (
  lists_edition_id INTEGER  NOT NULL,
  entity_edition_id INTEGER  NOT NULL,
  ownership_status_id INTEGER  NOT NULL,
  condition_type_id INTEGER  NOT NULL,
  edition_read_status_type_id INTEGER  NOT NULL,
  observation TEXT NULL,
  PRIMARY KEY(lists_edition_id, entity_edition_id),
  FOREIGN KEY(lists_edition_id)
    REFERENCES lists_edition(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_edition_id)
    REFERENCES entity_edition(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(edition_read_status_type_id)
    REFERENCES edition_read_status_type(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(condition_type_id)
    REFERENCES condition_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(ownership_status_id)
    REFERENCES ownership_status(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS lists_goods_list_goods (
  lists_goods_id INTEGER  NOT NULL,
  goods_id BIGINT  NOT NULL,
  ownership_status_id INTEGER  NOT NULL,
  box_condition_type_id INTEGER  NOT NULL,
  product_condition_type_id INTEGER  NOT NULL,
  observation TEXT NULL,
  PRIMARY KEY(lists_goods_id, goods_id),
  FOREIGN KEY(lists_goods_id)
    REFERENCES lists_goods(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(goods_id)
    REFERENCES goods(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(product_condition_type_id)
    REFERENCES product_condition_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(box_condition_type_id)
    REFERENCES box_condition_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(ownership_status_id)
    REFERENCES ownership_status(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS persona_unusual_features (
  id SERIAL,
  persona_id INTEGER  NOT NULL,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(persona_id)
    REFERENCES persona(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS persona_alias (
  id SERIAL,
  persona_id INTEGER  NOT NULL,
  alias_type_id INTEGER  NOT NULL,
  name VARCHAR NOT NULL,
  last_name VARCHAR NOT NULL DEFAULT "NO LAST NAME",
  PRIMARY KEY(id),
  FOREIGN KEY(persona_id)
    REFERENCES persona(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(alias_type_id)
    REFERENCES alias_type(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS persona_occupation (
  id SERIAL,
  persona_id INTEGER  NOT NULL,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(persona_id)
    REFERENCES persona(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS game_release (
  entity_release_id BIGSERIAL,
  emulate BOOLEAN NOT NULL DEFAULT FALSE,
  installation_instructions TEXT NULL,
  PRIMARY KEY(entity_release_id),
  FOREIGN KEY(entity_release_id)
    REFERENCES entity_release(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS persona_affiliation (
  id SERIAL,
  persona_id INTEGER  NOT NULL,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(persona_id)
    REFERENCES persona(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS persona_race (
  id SERIAL,
  persona_id INTEGER  NOT NULL,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(persona_id)
    REFERENCES persona(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS software_edition_has_version (
  software_edition_id INTEGER  NOT NULL,
  version_id INTEGER  NOT NULL,
  PRIMARY KEY(software_edition_id, version_id),
  FOREIGN KEY(software_edition_id)
    REFERENCES software_edition(entity_edition_id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(version_id)
    REFERENCES version(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS read_edition (
  entity_edition_id INTEGER  NOT NULL,
  print_type_id INTEGER  NOT NULL,
  pages_number INTEGER,
  chapters_number INTEGER  NULL,
  PRIMARY KEY(entity_edition_id),
  FOREIGN KEY(entity_edition_id)
    REFERENCES entity_edition(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(print_type_id)
    REFERENCES print_type(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS soundtrack_for_entity_edition (
  soundtrack_id INTEGER  NOT NULL,
  entity_edition_id INTEGER  NOT NULL,
  PRIMARY KEY(soundtrack_id, entity_edition_id),
  FOREIGN KEY(soundtrack_id)
    REFERENCES soundtrack(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_edition_id)
    REFERENCES entity_edition(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;
 
/* Maybe create in the future for entity_release */
CREATE TABLE IF NOT EXISTS entity_edition_launch_country (
  entity_edition_id INTEGER  NOT NULL,
  country_id INTEGER  NOT NULL,
  currency_id INTEGER  NOT NULL,
  launch_date DATE NOT NULL,
  launch_price DECIMAL NOT NULL,
  PRIMARY KEY(entity_edition_id, country_id),
  FOREIGN KEY(entity_edition_id)
    REFERENCES entity_edition(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(country_id)
    REFERENCES country(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION, 
	FOREIGN KEY(currency_id)
    REFERENCES currency(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS entity_edition_has_subtitle (
  subtitle_id INTEGER  NOT NULL,
  entity_edition_id INTEGER  NOT NULL,
  PRIMARY KEY(subtitle_id, entity_edition_id),
  FOREIGN KEY(subtitle_id)
    REFERENCES language(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(entity_edition_id)
    REFERENCES entity_edition(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS entity_edition_has_language (
  entity_edition_id INTEGER  NOT NULL,
  language_id INTEGER  NOT NULL,
  PRIMARY KEY(entity_edition_id, language_id),
  FOREIGN KEY(entity_edition_id)
    REFERENCES entity_edition(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(language_id)
    REFERENCES language(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS entity_release_has_version (
  entity_release_id BIGINT  NOT NULL,
  version_id INTEGER  NOT NULL,
  PRIMARY KEY(entity_release_id, version_id),
  FOREIGN KEY(entity_release_id)
    REFERENCES entity_release(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(version_id)
    REFERENCES version(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS entity_release_has_language (
  entity_release_id BIGINT  NOT NULL,
  language_id INTEGER  NOT NULL,
  PRIMARY KEY(entity_release_id, language_id),
  FOREIGN KEY(entity_release_id)
    REFERENCES entity_release(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(language_id)
    REFERENCES language(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

/* Check unique name for each entity_release_id*/

CREATE TABLE IF NOT EXISTS mod_release (
  id SERIAL,
  entity_release_id BIGINT  NOT NULL,
  mod_type_id INTEGER  NOT NULL,
  name VARCHAR UNIQUE NOT NULL,
  author VARCHAR NOT NULL,
  launch_date DATE NULL,
  description TEXT NULL,
  installation_instruction TEXT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(mod_type_id)
    REFERENCES mod_type(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_release_id)
    REFERENCES entity_release(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS mod_release_has_image (
  mod_release_id INTEGER  NOT NULL,
  image_id BIGINT  NOT NULL,
  PRIMARY KEY(mod_release_id, image_id),
  FOREIGN KEY(mod_release_id)
    REFERENCES mod_release(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(image_id)
    REFERENCES image(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS collaborator_provides_entity_release (
  collaborator_id INTEGER  NOT NULL,
  entity_release_id BIGINT  NOT NULL,
  collaborator_type_id INTEGER  NOT NULL,
  PRIMARY KEY(collaborator_id, entity_release_id),
  FOREIGN KEY(collaborator_id)
    REFERENCES collaborator(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_release_id)
    REFERENCES entity_release(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(collaborator_type_id)
    REFERENCES collaborator_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS collaborator_member_produces_entity_release (
  collaborator_member_id INTEGER  NOT NULL,
  entity_release_id BIGINT  NOT NULL,
  collaborator_member_type_id INTEGER  NOT NULL,
  PRIMARY KEY(collaborator_member_id, entity_release_id),
  FOREIGN KEY(collaborator_member_id)
    REFERENCES collaborator_member(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_release_id)
    REFERENCES entity_release(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(collaborator_member_type_id)
    REFERENCES function_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS entity_edition_has_company (
  company_id INTEGER  NOT NULL,
  entity_edition_id INTEGER  NOT NULL,
  company_function_type_id INTEGER  NOT NULL,
  PRIMARY KEY(company_id, entity_edition_id, company_function_type_id),
  FOREIGN KEY(company_id)
    REFERENCES company(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_edition_id)
    REFERENCES entity_edition(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(company_function_type_id)
    REFERENCES company_function_type(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS entity_has_company (
  company_id INTEGER  NOT NULL,
  entity_id BIGINT  NOT NULL,
  company_function_type_id INTEGER  NOT NULL,
  PRIMARY KEY(company_id, entity_id, company_function_type_id),
  FOREIGN KEY(company_id)
    REFERENCES company(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(company_function_type_id)
    REFERENCES company_function_type(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_id)
    REFERENCES entity(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS entity_edition_has_image (
  image_id BIGINT  NOT NULL,
  entity_edition_id INTEGER  NOT NULL,
  image_entity_edition_type_id INTEGER  NOT NULL,
  PRIMARY KEY(image_id, entity_edition_id),
  FOREIGN KEY(image_id)
    REFERENCES image(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_edition_id)
    REFERENCES entity_edition(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(image_entity_edition_type_id)
    REFERENCES image_entity_edition_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
;

/* not normalized table */
CREATE TABLE IF NOT EXISTS entity_has_image (
  image_id BIGINT  NOT NULL,
  entity_id INTEGER  NOT NULL,
  PRIMARY KEY(image_id, entity_id),
  FOREIGN KEY(image_id)
    REFERENCES image(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_id)
    REFERENCES entity(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS number_edition (
  id SERIAL,
  entity_edition_id INTEGER  NOT NULL,
  number_type_id INTEGER  NOT NULL,
  number VARCHAR  NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(number_type_id)
    REFERENCES number_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_edition_id)
    REFERENCES entity_edition(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS number_release (
  id SERIAL,
  number_release_id INTEGER NULL,
  entity_release_id BIGINT  NOT NULL,
  number_type_id INTEGER  NOT NULL,
  number VARCHAR  NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(number_type_id)
    REFERENCES number_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_release_id)
    REFERENCES entity_release(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(number_release_id)
    REFERENCES number_release(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS lists_release_list_entity_release (
  lists_release_id INTEGER  NOT NULL,
  entity_release_id BIGINT  NOT NULL,
  release_edition_read_status_type_id INTEGER  NOT NULL,
  release_ownership_type_id INTEGER  NOT NULL,
  local_storage VARCHAR NULL,
  PRIMARY KEY(lists_release_id, entity_release_id),
  FOREIGN KEY(lists_release_id)
    REFERENCES lists_release(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_release_id)
    REFERENCES entity_release(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(release_ownership_type_id)
    REFERENCES release_ownership_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(release_edition_read_status_type_id)
    REFERENCES release_edition_read_status_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS soundtrack_comments (
  id SERIAL,
  soundtrack_id INTEGER  NOT NULL,
  user_id INTEGER  NOT NULL,
  content TEXT NOT NULL,
  title VARCHAR NOT NULL,
  create_date timestamp without time zone NOT NULL DEFAULT now(),
  update_date timestamp without time zone NOT NULL DEFAULT now(),
  PRIMARY KEY(id),
  FOREIGN KEY(user_id)
    REFERENCES users(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(soundtrack_id)
    REFERENCES soundtrack(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;




CREATE TABLE IF NOT EXISTS audio_comments (
  id SERIAL,
  audio_id INTEGER  NOT NULL,
  user_id INTEGER  NOT NULL,
  content TEXT NOT NULL,
  title VARCHAR NOT NULL,
  create_date timestamp without time zone NOT NULL DEFAULT now(),
  update_date timestamp without time zone NOT NULL DEFAULT now(),
  PRIMARY KEY(id),
  FOREIGN KEY(user_id)
    REFERENCES users(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(audio_id)
    REFERENCES audio(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS company_comments (
  id SERIAL,
  company_id INTEGER  NOT NULL,
  user_id INTEGER  NOT NULL,
  content TEXT NOT NULL,
  title VARCHAR NOT NULL,
  create_date timestamp without time zone NOT NULL DEFAULT now(),
  update_date timestamp without time zone NOT NULL DEFAULT now(),
  PRIMARY KEY(id),
  FOREIGN KEY(user_id)
    REFERENCES users(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(company_id)
    REFERENCES company(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS people_comments (
  id SERIAL,
  people_id BIGINT  NOT NULL,
  user_id INTEGER  NOT NULL,
  content TEXT NOT NULL,
  title VARCHAR NOT NULL,
  create_date timestamp without time zone NOT NULL DEFAULT now(),
  update_date timestamp without time zone NOT NULL DEFAULT now(),
  PRIMARY KEY(id),
  FOREIGN KEY(user_id)
    REFERENCES users(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(people_id)
    REFERENCES people(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS goods_comments (
  id SERIAL,
  goods_id BIGINT  NOT NULL,
  user_id INTEGER  NOT NULL,
  content TEXT NOT NULL,
  title VARCHAR NOT NULL,
  create_date timestamp without time zone NOT NULL DEFAULT now(),
  update_date timestamp without time zone NOT NULL DEFAULT now(),
  PRIMARY KEY(id),
  FOREIGN KEY(user_id)
    REFERENCES users(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(goods_id)
    REFERENCES goods(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS collaborator_comments (
  id SERIAL,
  collaborator_id INTEGER  NOT NULL,
  user_id INTEGER  NOT NULL,
  content TEXT NOT NULL,
  title VARCHAR NOT NULL,
  create_date timestamp without time zone NOT NULL DEFAULT now(),
  update_date timestamp without time zone NOT NULL DEFAULT now(),
  PRIMARY KEY(id),
  FOREIGN KEY(user_id)
    REFERENCES users(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(collaborator_id)
    REFERENCES collaborator(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS entity_edition_comments (
  id SERIAL,
  entity_edition_id INTEGER  NOT NULL,
  user_id INTEGER  NOT NULL,
  content TEXT NOT NULL,
  title VARCHAR NOT NULL,
  create_date timestamp without time zone NOT NULL DEFAULT now(),
  update_date timestamp without time zone NOT NULL DEFAULT now(),
  PRIMARY KEY(id),
  FOREIGN KEY(user_id)
    REFERENCES users(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_edition_id)
    REFERENCES entity_edition(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS collection_comments (
  id SERIAL,
  collection_id BIGINT  NOT NULL,
  user_id INTEGER  NOT NULL,
  content TEXT NOT NULL,
  title VARCHAR NOT NULL,
  create_date timestamp without time zone NOT NULL DEFAULT now(),
  update_date timestamp without time zone NOT NULL DEFAULT now(),
  PRIMARY KEY(id),
  FOREIGN KEY(user_id)
    REFERENCES users(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(collection_id)
    REFERENCES collection(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS entity_release_comments (
  id SERIAL,
  entity_release_id BIGINT  NOT NULL,
  user_id INTEGER  NOT NULL,
  content TEXT NOT NULL,
  title VARCHAR NOT NULL,
  create_date timestamp without time zone NOT NULL DEFAULT now(),
  update_date timestamp without time zone NOT NULL DEFAULT now(),
  PRIMARY KEY(id),
  FOREIGN KEY(user_id)
    REFERENCES users(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_release_id)
    REFERENCES entity_release(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS entity_comments (
  id SERIAL,
  entity_id BIGINT  NOT NULL,
  user_id INTEGER  NOT NULL,
  content TEXT NOT NULL,
  title VARCHAR NOT NULL,
  create_date timestamp without time zone NOT NULL DEFAULT now(),
  update_date timestamp without time zone NOT NULL DEFAULT now(),
  PRIMARY KEY(id),
  FOREIGN KEY(user_id)
    REFERENCES users(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_id)
    REFERENCES entity(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS people_voice_persona (
  persona_id INTEGER NOT NULL,
  people_id BIGINT NOT NULL,
  language_id INTEGER NOT NULL,
  entity_id BIGINT NOT NULL,
  entity_edition_id INTEGER NULL,
  observation TEXT NULL,
  PRIMARY KEY(persona_id, people_id, language_id, entity_id),
  FOREIGN KEY(persona_id)
    REFERENCES persona(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(people_id)
    REFERENCES people(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(language_id)
    REFERENCES language(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_edition_id)
    REFERENCES entity_edition(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_id)
    REFERENCES entity(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS tag_user_filter (
  user_filter_id INTEGER  NOT NULL,
  tag_id INTEGER  NOT NULL,
  PRIMARY KEY(user_filter_id, tag_id),
  FOREIGN KEY(user_filter_id)
    REFERENCES user_filter(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(tag_id)
    REFERENCES tag(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS classification_user_filter (
  user_filter_id INTEGER  NOT NULL,
  classification_id INTEGER  NOT NULL,
  PRIMARY KEY(user_filter_id, classification_id),
  FOREIGN KEY(user_filter_id)
    REFERENCES user_filter(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(classification_id)
    REFERENCES classification_type(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS category_user_filter (
  user_filter_id INTEGER  NOT NULL,
  category_id INTEGER  NOT NULL,
  PRIMARY KEY(user_filter_id, category_id),
  FOREIGN KEY(user_filter_id)
    REFERENCES user_filter(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(category_id)
    REFERENCES category(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS persona_appear_on_entity (
  persona_id INTEGER  NOT NULL,
  entity_id BIGINT  NOT NULL,
  persona_alias_id BIGINT  NOT NULL,
  first_appear BOOL NOT NULL,
  PRIMARY KEY(persona_id, entity_id, persona_alias_id),
  FOREIGN KEY(persona_id)
    REFERENCES persona(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_id)
    REFERENCES entity(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
	 FOREIGN KEY(persona_alias_id)
    REFERENCES persona_alias(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS persona_has_image (
  image_id BIGINT  NOT NULL,
  persona_id BIGINT  NOT NULL,
  PRIMARY KEY(image_id, persona_id),
  FOREIGN KEY(image_id)
    REFERENCES image(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(persona_id)
    REFERENCES persona(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS company_has_image (
  image_id BIGINT  NOT NULL,
  company_id INTEGER  NOT NULL,
  image_company_type_id INTEGER  NOT NULL,
  PRIMARY KEY(image_id, company_id),
  FOREIGN KEY(image_id)
    REFERENCES image(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(company_id)
    REFERENCES company(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(image_company_type_id)
    REFERENCES image_company_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS people_voice_persona_on_number_edition (
  people_voice_persona_language_id INTEGER  NOT NULL,
  people_voice_persona_people_id BIGINT  NOT NULL,
  people_voice_persona_persona_id INTEGER  NOT NULL,
  people_voice_persona_entity_id INTEGER  NOT NULL,
  number_edition_id INTEGER  NOT NULL,
  PRIMARY KEY(people_voice_persona_language_id, people_voice_persona_people_id, people_voice_persona_persona_id, people_voice_persona_entity_id, number_edition_id),
  FOREIGN KEY(people_voice_persona_persona_id, people_voice_persona_people_id, people_voice_persona_language_id, people_voice_persona_entity_id)
    REFERENCES people_voice_persona(persona_id, people_id, language_id, entity_id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(number_edition_id)
    REFERENCES number_edition(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS requirements_has_driver (
  requirements_id INTEGER  NOT NULL,
  driver_id INTEGER  NOT NULL,
  PRIMARY KEY(requirements_id, driver_id),
  FOREIGN KEY(requirements_id)
    REFERENCES requirements(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(driver_id)
    REFERENCES driver(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS audio_has_image (
  audio_id INTEGER  NOT NULL,
  image_id BIGINT  NOT NULL,
  image_audio_type_id INTEGER  NOT NULL,
  PRIMARY KEY(audio_id, image_id),
  FOREIGN KEY(audio_id)
    REFERENCES audio(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(image_id)
    REFERENCES image(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(image_audio_type_id)
    REFERENCES image_audio_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS collaborator_has_image (
  collaborator_id INTEGER  NOT NULL,
  image_id BIGINT  NOT NULL,
  image_collaborator_type_id INTEGER  NOT NULL,
  PRIMARY KEY(collaborator_id, image_id),
  FOREIGN KEY(collaborator_id)
    REFERENCES collaborator(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(image_id)
    REFERENCES image(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(image_collaborator_type_id)
    REFERENCES image_collaborator_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS user_has_image (
  user_id INTEGER  NOT NULL,
  image_id BIGINT  NOT NULL,
  image_user_type_id INTEGER  NOT NULL,
  PRIMARY KEY(user_id, image_id),
  FOREIGN KEY(user_id)
    REFERENCES users(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(image_id)
    REFERENCES image(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(image_user_type_id)
    REFERENCES image_user_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS archive_url (
  id BIGSERIAL,
  url_type_id INTEGER  NOT NULL,
  archive_id BIGINT  NOT NULL,
  url VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(archive_id)
    REFERENCES archive(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(url_type_id)
    REFERENCES url_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS video_release (
  entity_release_id BIGINT  NOT NULL,
  video_codec_id INTEGER  NOT NULL,
  archive_container_id INTEGER  NOT NULL,
  duration VARCHAR NOT NULL,
  resolution VARCHAR NOT NULL,
  softsub BOOL NOT NULL,
  PRIMARY KEY(entity_release_id),
  FOREIGN KEY(entity_release_id)
    REFERENCES entity_release(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(archive_container_id)
    REFERENCES archive_container(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(video_codec_id)
    REFERENCES video_codec(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS video_release_has_audio_codec (
  audio_codec_id INTEGER  NOT NULL,
  video_release_entity_release_id BIGINT  NOT NULL,
  language_id INTEGER  NOT NULL,
  PRIMARY KEY(audio_codec_id, video_release_entity_release_id, language_id),
  FOREIGN KEY(audio_codec_id)
    REFERENCES audio_codec(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(video_release_entity_release_id)
    REFERENCES video_release(entity_release_id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(language_id)
    REFERENCES language(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS goods_alias (
  id SERIAL,
  language_id INTEGER  NOT NULL,
  alias_type_id INTEGER  NOT NULL,
  goods_id BIGINT  NOT NULL,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(goods_id)
    REFERENCES goods(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(alias_type_id)
    REFERENCES alias_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(language_id)
    REFERENCES language(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS figure (
  goods_id BIGINT  NOT NULL,
  figure_version_id INTEGER  NOT NULL,
  scale_id INTEGER  NOT NULL,
  PRIMARY KEY(goods_id),
  FOREIGN KEY(scale_id)
    REFERENCES scale(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(figure_version_id)
    REFERENCES figure_version(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(goods_id)
    REFERENCES goods(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS goods_description (
  id SERIAL,
  goods_id BIGINT  NOT NULL,
  language_id INTEGER  NOT NULL,
  description TEXT NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(goods_id)
    REFERENCES goods(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
FOREIGN KEY(language_id)
    REFERENCES language(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS goods_launch_country (
  country_id INTEGER  NOT NULL,
  goods_id BIGINT  NOT NULL,
  currency_id INTEGER  NOT NULL,
  launch_date DATE NOT NULL,
  launch_price DECIMAL NOT NULL,
  PRIMARY KEY(country_id, goods_id, currency_id),
  FOREIGN KEY(country_id)
    REFERENCES country(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(goods_id)
    REFERENCES goods(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(currency_id)
    REFERENCES currency(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS people_create_goods (
  people_id BIGINT  NOT NULL,
  goods_id BIGINT  NOT NULL,
  people_alias_id INTEGER  NOT NULL,
  create_type_id INTEGER  NOT NULL,
  PRIMARY KEY(people_id, goods_id, create_type_id),
  FOREIGN KEY(people_id)
    REFERENCES people(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(goods_id)
    REFERENCES goods(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(create_type_id)
    REFERENCES create_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(people_alias_id)
    REFERENCES people_alias(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS goods_has_image (
  image_id BIGINT  NOT NULL,
  goods_id BIGINT  NOT NULL,
  image_goods_type_id INTEGER  NOT NULL,
  PRIMARY KEY(image_id, goods_id),
  FOREIGN KEY(image_id)
    REFERENCES image(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(goods_id)
    REFERENCES goods(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(image_goods_type_id)
    REFERENCES image_goods_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS goods_has_shop_location (
  goods_id BIGINT  NOT NULL,
  shop_location_id INTEGER  NOT NULL,
  PRIMARY KEY(goods_id, shop_location_id),
  FOREIGN KEY(goods_id)
    REFERENCES goods(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(shop_location_id)
    REFERENCES shop_location(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS goods_has_tag (
  tag_id INTEGER  NOT NULL,
  goods_id BIGINT  NOT NULL,
  PRIMARY KEY(tag_id, goods_id),
  FOREIGN KEY(tag_id)
    REFERENCES tag(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(goods_id)
    REFERENCES goods(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS goods_has_shops (
  goods_id BIGINT  NOT NULL,
  shops_id INTEGER  NOT NULL,
  product_url VARCHAR NOT NULL,
  checked_last timestamp without time zone NOT NULL DEFAULT now(),
  PRIMARY KEY(goods_id, shops_id),
  FOREIGN KEY(goods_id)
    REFERENCES goods(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(shops_id)
    REFERENCES shops(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS goods_from_persona (
  goods_id BIGINT  NOT NULL,
  persona_id INTEGER  NOT NULL,
  PRIMARY KEY(goods_id, persona_id),
  FOREIGN KEY(goods_id)
    REFERENCES goods(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(persona_id)
    REFERENCES persona(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS goods_has_category (
  category_id INTEGER  NOT NULL,
  goods_id BIGINT  NOT NULL,
  PRIMARY KEY(category_id, goods_id),
  FOREIGN KEY(category_id)
    REFERENCES category(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(goods_id)
    REFERENCES goods(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS goods_has_material (
  goods_id BIGINT  NOT NULL,
  material_id INTEGER  NOT NULL,
  PRIMARY KEY(goods_id, material_id),
  FOREIGN KEY(goods_id)
    REFERENCES goods(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(material_id)
    REFERENCES material(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS goods_has_company (
  company_id INTEGER  NOT NULL,
  goods_id BIGINT  NOT NULL,
  company_function_type_id INTEGER  NOT NULL,
  PRIMARY KEY(company_id, goods_id, company_function_type_id),
  FOREIGN KEY(company_id)
    REFERENCES company(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(company_function_type_id)
    REFERENCES company_function_type(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(goods_id)
    REFERENCES goods(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS company_alias (
  id SERIAL,
  language_id INTEGER  NOT NULL,
  alias_type_id INTEGER  NOT NULL,
  company_id BIGINT  NOT NULL,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(company_id)
    REFERENCES company(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(alias_type_id)
    REFERENCES alias_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(language_id)
    REFERENCES language(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS collection_alias (
  id SERIAL,
  alias_type_id INTEGER  NOT NULL,
  collection_id BIGINT  NOT NULL,
  language_id INTEGER  NOT NULL,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(language_id)
    REFERENCES language(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(collection_id)
    REFERENCES collection(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(alias_type_id)
    REFERENCES alias_type(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
)
;

CREATE TABLE IF NOT EXISTS collection_wiki (
  id SERIAL,
  language_id INTEGER  NOT NULL,
  collection_id BIGINT  NOT NULL,
  name VARCHAR NOT NULL,
  url VARCHAR UNIQUE NOT NULL,
  PRIMARY KEY(id, language_id),
  FOREIGN KEY(collection_id)
    REFERENCES collection(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(language_id)
    REFERENCES language(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS persona_comments (
  id SERIAL,
  persona_id INTEGER  NOT NULL,
  user_id INTEGER  NOT NULL,
  content TEXT NOT NULL,
  title VARCHAR NOT NULL,
  create_date timestamp without time zone NOT NULL DEFAULT now(),
  update_date timestamp without time zone NOT NULL DEFAULT now(),
  PRIMARY KEY(id),
  FOREIGN KEY(user_id)
    REFERENCES users(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(persona_id)
    REFERENCES persona(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;

CREATE TABLE IF NOT EXISTS persona_has_tag (
  tag_id INTEGER  NOT NULL,
  persona_id BIGINT  NOT NULL,
  PRIMARY KEY(tag_id, persona_id),
  FOREIGN KEY(tag_id)
    REFERENCES tag(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(persona_id)
    REFERENCES persona(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
;