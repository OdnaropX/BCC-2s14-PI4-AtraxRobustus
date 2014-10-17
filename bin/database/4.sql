CREATE TABLE image_soundtrack_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE language (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  code VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE image_entity_edition_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE image_figure_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE lyric_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE mod_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE number_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE material (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE media_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE image (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  url VARCHAR NOT NULL,
  extension VARCHAR NOT NULL,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE edition_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE entity_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE driver (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  url_download VARCHAR NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE edition_read_status_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE figure_version (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE genre (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE hash_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE filter_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE function_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE ownership_status (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE software_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE soundtrack_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE shop_location_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE social_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  website VARCHAR NOT NULL,
  website_secure VARCHAR NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE spider_item (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  identify VARCHAR NOT NULL,
  url VARCHAR NOT NULL,
  complete_crawled BOOL NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE users (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  username VARCHAR NOT NULL,
  pass VARCHAR NOT NULL,
  gender SET NOT NULL,
  location VARCHAR NOT NULL,
  birthday DATE NOT NULL,
  signup_date DATETIME NOT NULL,
  activated BOOL NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE user_filter_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE stage_developer_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE tag (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  user_filter INTEGER UNSIGNED NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE shops (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  url VARCHAR NOT NULL,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE produces_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE product_condition_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE plataform_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE print_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE related_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE release_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE scale (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE release_ownership_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE release_read_status_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE condition_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE collaborator (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  irc VARCHAR NULL,
  description TEXT NOT NULL,
  create_date DATETIME NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE compose_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE company_function_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE classification_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE blood_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
);

CREATE TABLE audio_codec (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE collaborator_member (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  active BOOL NOT NULL DEFAULT 1,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE country (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  code VARCHAR NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE based_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE alias_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE box_condition_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE collection (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  description TEXT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE currency (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  symbol VARCHAR NOT NULL,
  code VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE create_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE category (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NOT NULL,
  user_filter INTEGER UNSIGNED NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE collaborator_type (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR NULL,
  PRIMARY KEY(id)
);

CREATE TABLE lists_figure (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  user_2_id INTEGER UNSIGNED NOT NULL,
  name VARCHAR NULL,
  create_date DATETIME NULL,
  PRIMARY KEY(id),
  INDEX lists_figure_FKIndex1(user_2_id),
  FOREIGN KEY(user_2_id)
    REFERENCES users(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
);

CREATE TABLE soundtrack (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  soundtrack_type_id INTEGER UNSIGNED NOT NULL,
  name VARCHAR NOT NULL,
  launch_year YEAR NOT NULL,
  PRIMARY KEY(id),
  INDEX soundtrack_FKIndex1(soundtrack_type_id),
  FOREIGN KEY(soundtrack_type_id)
    REFERENCES soundtrack_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE social (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  social_type_id INTEGER UNSIGNED NOT NULL,
  url VARCHAR NOT NULL,
  PRIMARY KEY(id),
  INDEX social_FKIndex1(social_type_id),
  FOREIGN KEY(social_type_id)
    REFERENCES social_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE company (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  country_id INTEGER UNSIGNED NOT NULL,
  name VARCHAR NOT NULL,
  social_name VARCHAR NULL,
  start_year YEAR NULL,
  website VARCHAR NULL,
  description TEXT NULL,
  create_date DATETIME NOT NULL,
  PRIMARY KEY(id),
  INDEX company_FKIndex1(country_id),
  FOREIGN KEY(country_id)
    REFERENCES country(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE collaborator_website (
  collaborator_id INTEGER UNSIGNED NOT NULL,
  website VARCHAR NOT NULL,
  PRIMARY KEY(collaborator_id, website),
  INDEX collaborator_website_FKIndex1(collaborator_id),
  FOREIGN KEY(collaborator_id)
    REFERENCES collaborator(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE event (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  currency_id INTEGER UNSIGNED NOT NULL,
  name VARCHAR NOT NULL,
  location VARCHAR NULL,
  website VARCHAR NULL,
  date DATE NOT NULL,
  duration INTEGER UNSIGNED NULL,
  free BOOL NOT NULL,
  edition VARCHAR NULL,
  PRIMARY KEY(id),
  INDEX event_FKIndex1(currency_id),
  FOREIGN KEY(currency_id)
    REFERENCES currency(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE user_email (
  users_id INTEGER UNSIGNED NOT NULL,
  email VARCHAR NOT NULL,
  INDEX user_email_FKIndex1(users_id),
  FOREIGN KEY(users_id)
    REFERENCES users(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
)
TYPE=InnoDB;

CREATE TABLE version (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  stage_developer_type_id INTEGER UNSIGNED NOT NULL,
  number VARCHAR NOT NULL,
  changelog TEXT NULL,
  PRIMARY KEY(id),
  INDEX version_FKIndex1(stage_developer_type_id),
  FOREIGN KEY(stage_developer_type_id)
    REFERENCES stage_developer_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE people (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  country_id INTEGER UNSIGNED NOT NULL,
  blood_type_id INTEGER UNSIGNED NOT NULL,
  website VARCHAR NULL,
  description TEXT NULL,
  PRIMARY KEY(id),
  INDEX people_FKIndex1(blood_type_id),
  INDEX people_FKIndex2(country_id),
  FOREIGN KEY(blood_type_id)
    REFERENCES blood_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(country_id)
    REFERENCES country(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE category_has_filter_type (
  category_id INTEGER UNSIGNED NOT NULL,
  user_filter_type_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(category_id, user_filter_type_id),
  INDEX category_has_filter_type_FKIndex1(category_id),
  INDEX category_has_filter_type_FKIndex2(user_filter_type_id),
  FOREIGN KEY(category_id)
    REFERENCES category(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(user_filter_type_id)
    REFERENCES filter_type(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE shops_operate_on_country (
  shops_id INTEGER UNSIGNED NOT NULL,
  country_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(shops_id, country_id),
  INDEX shops_has_country_FKIndex1(shops_id),
  INDEX shops_has_country_FKIndex2(country_id),
  FOREIGN KEY(shops_id)
    REFERENCES shops(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(country_id)
    REFERENCES country(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE soundtrack_comments (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  soundtrack_id INTEGER UNSIGNED NOT NULL,
  users_id INTEGER UNSIGNED NOT NULL,
  content TEXT NOT NULL,
  title VARCHAR NOT NULL,
  create_date DATETIME NOT NULL,
  update_date DATETIME NOT NULL,
  PRIMARY KEY(id),
  INDEX soundtrack_comments_FKIndex1(users_id),
  INDEX soundtrack_comments_FKIndex2(soundtrack_id),
  FOREIGN KEY(users_id)
    REFERENCES users(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(soundtrack_id)
    REFERENCES soundtrack(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE people_comments (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  people_id BIGINT UNSIGNED NOT NULL,
  users_id INTEGER UNSIGNED NOT NULL,
  content TEXT NOT NULL,
  title VARCHAR NOT NULL,
  create_date DATETIME NOT NULL,
  update_date DATETIME NOT NULL,
  PRIMARY KEY(id),
  INDEX people_comments_FKIndex1(users_id),
  INDEX people_comments_FKIndex2(people_id),
  FOREIGN KEY(users_id)
    REFERENCES users(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(people_id)
    REFERENCES people(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE collaborator_has_social (
  social_id INTEGER UNSIGNED NOT NULL,
  collaborator_id INTEGER UNSIGNED NOT NULL,
  create_date DATETIME NOT NULL,
  last_checked DATETIME NOT NULL,
  PRIMARY KEY(social_id, collaborator_id),
  INDEX social_has_collaborator_FKIndex1(social_id),
  INDEX social_has_collaborator_FKIndex2(collaborator_id),
  FOREIGN KEY(social_id)
    REFERENCES social(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(collaborator_id)
    REFERENCES collaborator(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE people_nacionalization (
  people_id BIGINT UNSIGNED NOT NULL,
  country_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(people_id, country_id),
  INDEX people_has_country_FKIndex1(people_id),
  INDEX people_has_country_FKIndex2(country_id),
  FOREIGN KEY(people_id)
    REFERENCES people(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(country_id)
    REFERENCES country(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE collaborator_has_member (
  collaborator_id INTEGER UNSIGNED NOT NULL,
  collaborator_member_id INTEGER UNSIGNED NOT NULL,
  founder BOOL NOT NULL DEFAULT 0,
  PRIMARY KEY(collaborator_id, collaborator_member_id),
  INDEX collaborator_has_member_FKIndex1(collaborator_id),
  INDEX collaborator_has_member_FKIndex2(collaborator_member_id),
  FOREIGN KEY(collaborator_id)
    REFERENCES collaborator(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(collaborator_member_id)
    REFERENCES collaborator_member(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
);

CREATE TABLE people_has_image (
  image_id BIGINT UNSIGNED NOT NULL,
  people_id BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY(image_id, people_id),
  INDEX image_has_people_FKIndex1(image_id),
  INDEX image_has_people_FKIndex2(people_id),
  FOREIGN KEY(image_id)
    REFERENCES image(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(people_id)
    REFERENCES people(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE people_has_social (
  social_id INTEGER UNSIGNED NOT NULL,
  people_id BIGINT UNSIGNED NOT NULL,
  last_checked DATETIME NOT NULL,
  create_date DATETIME NOT NULL,
  PRIMARY KEY(social_id, people_id),
  INDEX social_has_people_FKIndex1(social_id),
  INDEX social_has_people_FKIndex2(people_id),
  FOREIGN KEY(social_id)
    REFERENCES social(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(people_id)
    REFERENCES people(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE tag_has_filter_type (
  user_filter_type_id INTEGER UNSIGNED NOT NULL,
  tag_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(user_filter_type_id, tag_id),
  INDEX filter_type_has_tag_FKIndex1(user_filter_type_id),
  INDEX filter_type_has_tag_FKIndex2(tag_id),
  FOREIGN KEY(user_filter_type_id)
    REFERENCES filter_type(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(tag_id)
    REFERENCES tag(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE audio (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  country_id INTEGER UNSIGNED NOT NULL,
  audio_codec_id INTEGER UNSIGNED NOT NULL,
  name VARCHAR NOT NULL,
  duration TIME NULL,
  bitrate INTEGER UNSIGNED NULL,
  PRIMARY KEY(id),
  INDEX audio_FKIndex1(audio_codec_id),
  INDEX audio_FKIndex2(country_id),
  FOREIGN KEY(audio_codec_id)
    REFERENCES audio_codec(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(country_id)
    REFERENCES country(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE country_has_currency (
  currency_id INTEGER UNSIGNED NOT NULL,
  country_id INTEGER UNSIGNED NOT NULL,
  main BOOL NOT NULL,
  PRIMARY KEY(currency_id, country_id),
  INDEX currency_has_country_FKIndex1(currency_id),
  INDEX currency_has_country_FKIndex2(country_id),
  FOREIGN KEY(currency_id)
    REFERENCES currency(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(country_id)
    REFERENCES country(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE country_has_language (
  language_id INTEGER UNSIGNED NOT NULL,
  country_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(language_id, country_id),
  INDEX language_has_country_FKIndex1(language_id),
  INDEX language_has_country_FKIndex2(country_id),
  FOREIGN KEY(language_id)
    REFERENCES language(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(country_id)
    REFERENCES country(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE user_filter (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  user_filter_type_id INTEGER UNSIGNED NOT NULL,
  users_id INTEGER UNSIGNED NOT NULL,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id),
  INDEX filtro_FKIndex1(users_id),
  INDEX user_filter_FKIndex3(user_filter_type_id),
  FOREIGN KEY(users_id)
    REFERENCES users(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(user_filter_type_id)
    REFERENCES user_filter_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE users_has_social (
  users_id INTEGER UNSIGNED NOT NULL,
  social_id INTEGER UNSIGNED NOT NULL,
  last_checked DATETIME NOT NULL,
  create_date DATETIME NOT NULL,
  PRIMARY KEY(users_id, social_id),
  INDEX users_has_social_FKIndex1(users_id),
  INDEX users_has_social_FKIndex2(social_id),
  FOREIGN KEY(users_id)
    REFERENCES users(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(social_id)
    REFERENCES social(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE company_has_country (
  country_id INTEGER UNSIGNED NOT NULL,
  company_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(country_id, company_id),
  INDEX country_has_company_FKIndex1(country_id),
  INDEX country_has_company_FKIndex2(company_id),
  FOREIGN KEY(country_id)
    REFERENCES country(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(company_id)
    REFERENCES company(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE company_comments (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  company_id INTEGER UNSIGNED NOT NULL,
  users_id INTEGER UNSIGNED NOT NULL,
  content TEXT NOT NULL,
  title VARCHAR NOT NULL,
  create_date DATETIME NOT NULL,
  update_date DATETIME NOT NULL,
  PRIMARY KEY(id),
  INDEX company_comments_FKIndex1(users_id),
  INDEX company_comments_FKIndex2(company_id),
  FOREIGN KEY(users_id)
    REFERENCES users(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(company_id)
    REFERENCES company(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE company_has_social (
  social_id INTEGER UNSIGNED NOT NULL,
  company_id INTEGER UNSIGNED NOT NULL,
  last_checked DATETIME NOT NULL,
  create_date DATETIME NOT NULL,
  PRIMARY KEY(social_id, company_id),
  INDEX social_has_company_FKIndex1(social_id),
  INDEX social_has_company_FKIndex2(company_id),
  FOREIGN KEY(social_id)
    REFERENCES social(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(company_id)
    REFERENCES company(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE audio_comments (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  audio_id INTEGER UNSIGNED NOT NULL,
  users_id INTEGER UNSIGNED NOT NULL,
  content TEXT NOT NULL,
  title VARCHAR NOT NULL,
  create_date DATETIME NOT NULL,
  update_date DATETIME NOT NULL,
  PRIMARY KEY(id),
  INDEX audio_comments_FKIndex1(users_id),
  INDEX audio_comments_FKIndex2(audio_id),
  FOREIGN KEY(users_id)
    REFERENCES users(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(audio_id)
    REFERENCES audio(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE lists_edition (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  entity_type_id INTEGER UNSIGNED NOT NULL,
  user_2_id INTEGER UNSIGNED NOT NULL,
  name VARCHAR NOT NULL,
  create_date DATETIME NOT NULL,
  PRIMARY KEY(id),
  INDEX lists_edition_FKIndex1(user_2_id),
  INDEX lists_edition_FKIndex2(entity_type_id),
  FOREIGN KEY(user_2_id)
    REFERENCES users(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_type_id)
    REFERENCES entity_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE lists_release (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  entity_type_id INTEGER UNSIGNED NOT NULL,
  user_2_id INTEGER UNSIGNED NOT NULL,
  name VARCHAR NOT NULL,
  create_date DATETIME NOT NULL,
  PRIMARY KEY(id),
  INDEX lists_release_FKIndex1(user_2_id),
  INDEX lists_release_FKIndex2(entity_type_id),
  FOREIGN KEY(user_2_id)
    REFERENCES users(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_type_id)
    REFERENCES entity_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE soundtrack_has_audio (
  soundtrack_id INTEGER UNSIGNED NOT NULL,
  audio_id INTEGER UNSIGNED NOT NULL,
  exclusive BOOL NULL,
  PRIMARY KEY(soundtrack_id, audio_id),
  INDEX soundtrack_has_audio_FKIndex1(soundtrack_id),
  INDEX soundtrack_has_audio_FKIndex2(audio_id),
  FOREIGN KEY(soundtrack_id)
    REFERENCES soundtrack(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(audio_id)
    REFERENCES audio(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
);

CREATE TABLE audio_has_genre_type (
  audio_id INTEGER UNSIGNED NOT NULL,
  genre_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(audio_id, genre_id),
  INDEX genre_type_has_audio_FKIndex2(audio_id),
  INDEX audio_has_genre_type_FKIndex3(genre_id),
  FOREIGN KEY(audio_id)
    REFERENCES audio(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(genre_id)
    REFERENCES genre(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE soundtrack_integrate_collection (
  collection_id INTEGER UNSIGNED NOT NULL,
  soundtrack_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(collection_id, soundtrack_id),
  INDEX collection_has_soundtrack_FKIndex1(collection_id),
  INDEX collection_has_soundtrack_FKIndex2(soundtrack_id),
  FOREIGN KEY(collection_id)
    REFERENCES collection(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(soundtrack_id)
    REFERENCES soundtrack(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE company_owner_collection (
  company_id INTEGER UNSIGNED NOT NULL,
  collection_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(company_id, collection_id),
  INDEX company_has_collection_FKIndex1(company_id),
  INDEX company_has_collection_FKIndex2(collection_id),
  FOREIGN KEY(company_id)
    REFERENCES company(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(collection_id)
    REFERENCES collection(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE company_sponsors_event (
  company_id INTEGER UNSIGNED NOT NULL,
  event_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(company_id, event_id),
  INDEX company_has_event_FKIndex1(company_id),
  INDEX company_has_event_FKIndex2(event_id),
  FOREIGN KEY(company_id)
    REFERENCES company(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(event_id)
    REFERENCES event(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE soundtrack_has_image (
  soundtrack_id INTEGER UNSIGNED NOT NULL,
  image_id BIGINT UNSIGNED NOT NULL,
  image_soundtrack_type_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(soundtrack_id, image_id),
  INDEX soundtrack_has_image_FKIndex1(soundtrack_id),
  INDEX soundtrack_has_image_FKIndex2(image_id),
  INDEX soundtrack_has_image_FKIndex3(image_soundtrack_type_id),
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
TYPE=InnoDB;

CREATE TABLE lyrics (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  lyric_type_id INTEGER UNSIGNED NOT NULL,
  user_2_id INTEGER UNSIGNED NOT NULL,
  audio_id INTEGER UNSIGNED NOT NULL,
  language_id INTEGER UNSIGNED NOT NULL,
  lyric TEXT NOT NULL,
  title VARCHAR NULL,
  PRIMARY KEY(id),
  INDEX lyrics_FKIndex1(language_id),
  INDEX lyrics_FKIndex2(audio_id),
  INDEX lyrics_FKIndex3(user_2_id),
  INDEX lyrics_FKIndex4(lyric_type_id),
  FOREIGN KEY(language_id)
    REFERENCES language(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(audio_id)
    REFERENCES audio(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(user_2_id)
    REFERENCES users(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(lyric_type_id)
    REFERENCES lyric_type(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE entity (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  entity_type_id INTEGER UNSIGNED NOT NULL,
  classification_type_id INTEGER UNSIGNED NOT NULL,
  collection_id INTEGER UNSIGNED NOT NULL,
  language_id INTEGER UNSIGNED NOT NULL,
  country_id INTEGER UNSIGNED NOT NULL,
  launch_year YEAR NOT NULL,
  collection_started BOOL NOT NULL,
  PRIMARY KEY(id),
  INDEX entity_FKIndex1(country_id),
  INDEX entity_FKIndex2(language_id),
  INDEX entity_FKIndex3(collection_id),
  INDEX entity_FKIndex4(classification_type_id),
  INDEX entity_FKIndex5(entity_type_id),
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
TYPE=InnoDB;

CREATE TABLE figure (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  entity_id BIGINT UNSIGNED NOT NULL,
  figure_version_id INTEGER UNSIGNED NOT NULL,
  currency_id INTEGER UNSIGNED NOT NULL,
  scale_id INTEGER UNSIGNED NOT NULL,
  country_id INTEGER UNSIGNED NOT NULL,
  height TINYINT UNSIGNED NOT NULL,
  width TINYINT UNSIGNED NULL,
  weight DECIMAL NULL,
  launch_price DECIMAL NOT NULL,
  release_date DATE NOT NULL,
  observation TEXT NULL,
  PRIMARY KEY(id),
  INDEX figure_FKIndex2(country_id),
  INDEX figure_FKIndex3(scale_id),
  INDEX figure_FKIndex4(currency_id),
  INDEX figure_FKIndex5(figure_version_id),
  INDEX figure_FKIndex5(entity_id),
  FOREIGN KEY(country_id)
    REFERENCES country(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(scale_id)
    REFERENCES scale(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(currency_id)
    REFERENCES currency(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(figure_version_id)
    REFERENCES figure_version(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_id)
    REFERENCES entity(id)
      ON DELETE SET NULL
      ON UPDATE SET NULL
)
TYPE=InnoDB;

CREATE TABLE archive (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  version_id INTEGER UNSIGNED NOT NULL,
  name VARCHAR NOT NULL,
  url VARCHAR NOT NULL,
  size INTEGER UNSIGNED NOT NULL,
  extension VARCHAR NOT NULL,
  PRIMARY KEY(id),
  INDEX archive_FKIndex1(version_id),
  FOREIGN KEY(version_id)
    REFERENCES version(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE requirements (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  version_id INTEGER UNSIGNED NOT NULL,
  video_board VARCHAR NOT NULL,
  processor VARCHAR NOT NULL,
  memory VARCHAR NOT NULL,
  hd_storage VARCHAR NOT NULL,
  PRIMARY KEY(id),
  INDEX requirements_FKIndex1(version_id),
  FOREIGN KEY(version_id)
    REFERENCES version(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE audio_has_language (
  audio_id INTEGER UNSIGNED NOT NULL,
  language_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(audio_id, language_id),
  INDEX audio_has_language_FKIndex1(audio_id),
  INDEX audio_has_language_FKIndex2(language_id),
  FOREIGN KEY(audio_id)
    REFERENCES audio(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(language_id)
    REFERENCES language(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE people_alias (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  alias_type_id INTEGER UNSIGNED NOT NULL,
  people_id BIGINT UNSIGNED NOT NULL,
  name VARCHAR NOT NULL,
  lastname VARCHAR NULL,
  PRIMARY KEY(id),
  INDEX alias_FKIndex1(people_id),
  INDEX people_alias_FKIndex2(alias_type_id),
  FOREIGN KEY(people_id)
    REFERENCES people(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(alias_type_id)
    REFERENCES alias_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE category_user_filter (
  user_filter_id INTEGER UNSIGNED NOT NULL,
  category_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(user_filter_id),
  INDEX category_user_filter_FKIndex1(user_filter_id),
  INDEX category_user_filter_FKIndex2(category_id),
  FOREIGN KEY(user_filter_id)
    REFERENCES user_filter(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(category_id)
    REFERENCES category(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
);



CREATE TABLE persona (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  blood_type_id INTEGER UNSIGNED NOT NULL,
  entity_id BIGINT UNSIGNED NOT NULL,
  gender SET NULL,
  height INTEGER UNSIGNED NULL,
  weight DECIMAL NULL,
  eyes_color VARCHAR NULL,
  hair_color VARCHAR NULL,
  birthday DATETIME NULL,
  PRIMARY KEY(id),
  INDEX persona_FKIndex1(entity_id),
  INDEX persona_FKIndex2(blood_type_id),
  FOREIGN KEY(entity_id)
    REFERENCES entity(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(blood_type_id)
    REFERENCES blood_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE classification_user_filter (
  user_filter_id INTEGER UNSIGNED NOT NULL,
  classification_type_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(user_filter_id),
  INDEX classification_user_filter_FKIndex1(user_filter_id),
  INDEX classification_user_filter_FKIndex2(classification_type_id),
  FOREIGN KEY(user_filter_id)
    REFERENCES user_filter(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(classification_type_id)
    REFERENCES classification_type(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE entity_has_tag (
  tag_id INTEGER UNSIGNED NOT NULL,
  entity_id BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY(tag_id, entity_id),
  INDEX tag_has_entity_FKIndex1(tag_id),
  INDEX tag_has_entity_FKIndex2(entity_id),
  FOREIGN KEY(tag_id)
    REFERENCES tag(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_id)
    REFERENCES entity(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE entity_wiki (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  language_id INTEGER UNSIGNED NOT NULL,
  entity_id BIGINT UNSIGNED NOT NULL,
  name VARCHAR NOT NULL,
  url VARCHAR NOT NULL,
  PRIMARY KEY(id, language_id),
  INDEX entity_wiki_FKIndex1(entity_id),
  INDEX entity_wiki_FKIndex2(language_id),
  FOREIGN KEY(entity_id)
    REFERENCES entity(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(language_id)
    REFERENCES language(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE entity_synopse (
  entity_id BIGINT UNSIGNED NOT NULL,
  language_id INTEGER UNSIGNED NOT NULL,
  content TEXT NOT NULL,
  PRIMARY KEY(entity_id, language_id),
  INDEX enity_synopse_FKIndex1(entity_id),
  INDEX entity_synopse_FKIndex2(language_id),
  FOREIGN KEY(entity_id)
    REFERENCES entity(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(language_id)
    REFERENCES language(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE tag_user_filter (
  user_filter_id INTEGER UNSIGNED NOT NULL,
  tag_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(user_filter_id),
  INDEX tag_user_filter_FKIndex1(user_filter_id),
  INDEX tag_user_filter_FKIndex2(tag_id),
  FOREIGN KEY(user_filter_id)
    REFERENCES user_filter(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(tag_id)
    REFERENCES tag(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE entity_description (
  language_id INTEGER UNSIGNED NOT NULL,
  entity_id BIGINT UNSIGNED NOT NULL,
  description TEXT NOT NULL,
  PRIMARY KEY(language_id, entity_id),
  INDEX entity_description_FKIndex1(entity_id),
  INDEX entity_description_FKIndex2(language_id),
  FOREIGN KEY(entity_id)
    REFERENCES entity(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(language_id)
    REFERENCES language(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE entity_has_category (
  entity_id BIGINT UNSIGNED NOT NULL,
  category_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(entity_id, category_id),
  INDEX entity_has_category_FKIndex1(entity_id),
  INDEX entity_has_category_FKIndex2(category_id),
  FOREIGN KEY(entity_id)
    REFERENCES entity(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(category_id)
    REFERENCES category(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE figure_comments (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  figure_id BIGINT UNSIGNED NOT NULL,
  users_id INTEGER UNSIGNED NOT NULL,
  content TEXT NOT NULL,
  title VARCHAR NOT NULL,
  create_date DATETIME NOT NULL,
  update_date DATETIME NOT NULL,
  PRIMARY KEY(id),
  INDEX figure_comments_FKIndex1(users_id),
  INDEX figure_comments_FKIndex2(figure_id),
  FOREIGN KEY(users_id)
    REFERENCES users(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(figure_id)
    REFERENCES figure(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE figure_has_material (
  figure_id BIGINT UNSIGNED NOT NULL,
  material_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(figure_id, material_id),
  INDEX figure_has_material_FKIndex1(figure_id),
  INDEX figure_has_material_FKIndex2(material_id),
  FOREIGN KEY(figure_id)
    REFERENCES figure(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(material_id)
    REFERENCES material(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE figure_has_shops (
  figure_id BIGINT UNSIGNED NOT NULL,
  shops_id INTEGER UNSIGNED NOT NULL,
  product_url VARCHAR NOT NULL,
  checked_last DATETIME NULL,
  PRIMARY KEY(figure_id, shops_id),
  INDEX figure_has_shops_FKIndex1(figure_id),
  INDEX figure_has_shops_FKIndex2(shops_id),
  FOREIGN KEY(figure_id)
    REFERENCES figure(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(shops_id)
    REFERENCES shops(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE figure_from_persona (
  figure_id BIGINT UNSIGNED NOT NULL,
  persona_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(figure_id, persona_id),
  INDEX figure_has_persona_FKIndex1(figure_id),
  INDEX figure_has_persona_FKIndex2(persona_id),
  FOREIGN KEY(figure_id)
    REFERENCES figure(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(persona_id)
    REFERENCES persona(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE figure_has_category (
  category_id INTEGER UNSIGNED NOT NULL,
  figure_id BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY(category_id, figure_id),
  INDEX category_has_figure_FKIndex1(category_id),
  INDEX category_has_figure_FKIndex2(figure_id),
  FOREIGN KEY(category_id)
    REFERENCES category(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(figure_id)
    REFERENCES figure(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE figure_has_shop_location (
  figure_id BIGINT UNSIGNED NOT NULL,
  shop_location_type_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(figure_id, shop_location_type_id),
  INDEX figure_has_shop_location_FKIndex1(figure_id),
  INDEX figure_has_shop_location_FKIndex2(shop_location_type_id),
  FOREIGN KEY(figure_id)
    REFERENCES figure(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(shop_location_type_id)
    REFERENCES shop_location_type(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE hash (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  hash_type_id INTEGER UNSIGNED NOT NULL,
  archive_id BIGINT UNSIGNED NOT NULL,
  code TEXT NOT NULL,
  create_date DATETIME NOT NULL,
  PRIMARY KEY(id),
  INDEX hash_FKIndex2(archive_id),
  INDEX hash_FKIndex2(hash_type_id),
  FOREIGN KEY(archive_id)
    REFERENCES archive(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(hash_type_id)
    REFERENCES hash_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE figure_has_tag (
  tag_id INTEGER UNSIGNED NOT NULL,
  figure_id BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY(tag_id, figure_id),
  INDEX tag_has_figure_FKIndex1(tag_id),
  INDEX tag_has_figure_FKIndex2(figure_id),
  FOREIGN KEY(tag_id)
    REFERENCES tag(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(figure_id)
    REFERENCES figure(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE figure_has_image (
  image_id BIGINT UNSIGNED NOT NULL,
  figure_id BIGINT UNSIGNED NOT NULL,
  image_figure_type_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(image_id, figure_id),
  INDEX image_has_figure_FKIndex1(image_id),
  INDEX image_has_figure_FKIndex2(figure_id),
  INDEX image_has_figure_FKIndex3(image_figure_type_id),
  FOREIGN KEY(image_id)
    REFERENCES image(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(figure_id)
    REFERENCES figure(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(image_figure_type_id)
    REFERENCES image_figure_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE entity_based_entity (
  entity_id BIGINT UNSIGNED NOT NULL,
  other_entity_id INTEGER UNSIGNED NOT NULL,
  based_type_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(entity_id, other_entity_id),
  INDEX entity_has_entity_FKIndex1(entity_id),
  INDEX entity_has_entity_FKIndex2(entity_id),
  INDEX entity_has_entity_FKIndex3(based_type_id),
  FOREIGN KEY(entity_id)
    REFERENCES entity(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_id)
    REFERENCES entity(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(based_type_id)
    REFERENCES based_type(id)
      ON DELETE SET DEFAULT
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE entity_alias (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  people_alias_type_id INTEGER UNSIGNED NOT NULL,
  entity_id BIGINT UNSIGNED NOT NULL,
  language_id INTEGER UNSIGNED NOT NULL,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id),
  INDEX entity_alias_FKIndex1(language_id),
  INDEX entity_alias_FKIndex2(entity_id),
  INDEX entity_alias_FKIndex3(people_alias_type_id),
  FOREIGN KEY(language_id)
    REFERENCES language(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_id)
    REFERENCES entity(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(people_alias_type_id)
    REFERENCES alias_type(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE persona_related_persona (
  persona_id INTEGER UNSIGNED NOT NULL,
  related_type_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(persona_id),
  INDEX persona_has_persona_FKIndex1(persona_id),
  INDEX persona_has_persona_FKIndex2(persona_id),
  INDEX persona_related_persona_FKIndex3(related_type_id),
  FOREIGN KEY(persona_id)
    REFERENCES persona(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(persona_id)
    REFERENCES persona(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(related_type_id)
    REFERENCES related_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE entity_has_company (
  company_id INTEGER UNSIGNED NOT NULL,
  entity_id BIGINT UNSIGNED NOT NULL,
  company_function_type_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(company_id, entity_id, company_function_type_id),
  INDEX company_has_figure_FKIndex1(company_id),
  INDEX company_has_entity_FKIndex3(company_function_type_id),
  INDEX company_has_entity_FKIndex3(entity_id),
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
TYPE=InnoDB;

CREATE TABLE entity_edition (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  edition_type_id INTEGER UNSIGNED NOT NULL,
  event_id INTEGER UNSIGNED NOT NULL,
  entity_id BIGINT UNSIGNED NOT NULL,
  title VARCHAR NULL,
  free BOOL NULL,
  release_description TEXT NULL,
  censored BOOL NULL,
  code VARCHAR NULL,
  complement_code VARCHAR NULL,
  height INTEGER UNSIGNED NULL,
  width INTEGER UNSIGNED NULL,
  depth INTEGER UNSIGNED NULL,
  weight DECIMAL NULL,
  subtitle VARCHAR NULL,
  PRIMARY KEY(id),
  INDEX entity_edition_FKIndex1(entity_id),
  INDEX entity_edition_FKIndex2(event_id),
  INDEX entity_edition_FKIndex3(edition_type_id),
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

CREATE TABLE entity_release (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  entity_id BIGINT UNSIGNED NOT NULL,
  release_type_id INTEGER UNSIGNED NOT NULL,
  country_id INTEGER UNSIGNED NOT NULL,
  entity_edition_id INTEGER UNSIGNED NOT NULL,
  description TEXT NULL,
  release_date DATETIME NOT NULL,
  PRIMARY KEY(id),
  INDEX entity_release_FKIndex1(entity_edition_id),
  INDEX entity_release_FKIndex2(country_id),
  INDEX entity_release_FKIndex3(release_type_id),
  INDEX entity_release_FKIndex4(entity_id),
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
TYPE=InnoDB;

CREATE TABLE people_create_figure (
  people_id BIGINT UNSIGNED NOT NULL,
  figure_id BIGINT UNSIGNED NOT NULL,
  people_alias_id INTEGER UNSIGNED NOT NULL,
  create_type_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(people_id, figure_id),
  INDEX people_produces_figure_FKIndex1(people_id),
  INDEX people_produces_figure_FKIndex2(figure_id),
  INDEX people_produces_figure_FKIndex3(create_type_id),
  INDEX people_produces_figure_FKIndex4(people_alias_id),
  FOREIGN KEY(people_id)
    REFERENCES people(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(figure_id)
    REFERENCES figure(id)
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
TYPE=InnoDB;

CREATE TABLE software_edition (
  entity_edition_id INTEGER UNSIGNED NOT NULL,
  plataform_type_id INTEGER UNSIGNED NOT NULL,
  software_type_id INTEGER UNSIGNED NOT NULL,
  media_type_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(entity_edition_id),
  INDEX software_edition_FKIndex1(entity_edition_id),
  INDEX software_edition_FKIndex3(media_type_id),
  INDEX software_edition_FKIndex4(software_type_id),
  INDEX software_edition_FKIndex5(plataform_type_id),
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
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE people_produces_entity (
  people_id BIGINT UNSIGNED NOT NULL,
  entity_id BIGINT UNSIGNED NOT NULL,
  people_alias_id INTEGER UNSIGNED NOT NULL,
  create_type_2_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(people_id, entity_id),
  INDEX people_has_entity_FKIndex1(people_id),
  INDEX people_has_entity_FKIndex2(entity_id),
  INDEX people_produces_entity_FKIndex3(create_type_2_id),
  INDEX people_produces_entity_FKIndex4(people_alias_id),
  FOREIGN KEY(people_id)
    REFERENCES people(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_id)
    REFERENCES entity(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(create_type_2_id)
    REFERENCES produces_type(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(people_alias_id)
    REFERENCES people_alias(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE lists_release_list_entity_release (
  lists_release_id INTEGER UNSIGNED NOT NULL,
  entity_release_id BIGINT UNSIGNED NOT NULL,
  release_read_status_type_id INTEGER UNSIGNED NOT NULL,
  release_ownership_type_id INTEGER UNSIGNED NOT NULL,
  local_storage VARCHAR NULL,
  PRIMARY KEY(lists_release_id, entity_release_id),
  INDEX lists_release_has_entity_release_FKIndex1(lists_release_id),
  INDEX lists_release_has_entity_release_FKIndex2(entity_release_id),
  INDEX lists_release_list_entity_release_FKIndex3(release_ownership_type_id),
  INDEX lists_release_list_entity_release_FKIndex4(release_read_status_type_id),
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
  FOREIGN KEY(release_read_status_type_id)
    REFERENCES release_read_status_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE people_compose_audio (
  audio_id INTEGER UNSIGNED NOT NULL,
  people_id BIGINT UNSIGNED NOT NULL,
  people_alias_id INTEGER UNSIGNED NOT NULL,
  compose_type_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(audio_id, people_id),
  INDEX audio_has_people_FKIndex1(audio_id),
  INDEX audio_has_people_FKIndex2(people_id),
  INDEX people_compose_audio_FKIndex3(compose_type_id),
  INDEX people_compose_audio_FKIndex4(people_alias_id),
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
TYPE=InnoDB;

CREATE TABLE lists_figure_list_figure (
  lists_figure_id INTEGER UNSIGNED NOT NULL,
  figure_id BIGINT UNSIGNED NOT NULL,
  ownership_status_id INTEGER UNSIGNED NOT NULL,
  box_condition_type_id INTEGER UNSIGNED NOT NULL,
  product_condition_type_id INTEGER UNSIGNED NOT NULL,
  observation TEXT NULL,
  PRIMARY KEY(lists_figure_id, figure_id),
  INDEX lists_figure_has_figure_FKIndex1(lists_figure_id),
  INDEX lists_figure_has_figure_FKIndex2(figure_id),
  INDEX lists_figure_list_figure_FKIndex3(product_condition_type_id),
  INDEX lists_figure_list_figure_FKIndex4(box_condition_type_id),
  INDEX lists_figure_list_figure_FKIndex5(ownership_status_id),
  FOREIGN KEY(lists_figure_id)
    REFERENCES lists_figure(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(figure_id)
    REFERENCES figure(id)
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
TYPE=InnoDB;

CREATE TABLE people_voice_persona (
  persona_id INTEGER UNSIGNED NOT NULL,
  people_id BIGINT UNSIGNED NOT NULL,
  language_id INTEGER UNSIGNED NOT NULL,
  entity_id BIGINT UNSIGNED NOT NULL,
  entity_edition_id INTEGER UNSIGNED NOT NULL,
  observation TEXT NULL,
  PRIMARY KEY(persona_id, people_id, language_id),
  INDEX persona_has_people_FKIndex1(persona_id),
  INDEX persona_has_people_FKIndex2(people_id),
  INDEX people_voice_persona_FKIndex3(language_id),
  INDEX people_voice_persona_FKIndex4(entity_edition_id),
  INDEX people_voice_persona_FKIndex5(entity_id),
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

CREATE TABLE lists_edition_list_entity_edition (
  lists_edition_id INTEGER UNSIGNED NOT NULL,
  entity_edition_id INTEGER UNSIGNED NOT NULL,
  ownership_status_id INTEGER UNSIGNED NOT NULL,
  condition_type_id INTEGER UNSIGNED NOT NULL,
  edition_read_status_type_id INTEGER UNSIGNED NOT NULL,
  observation TEXT NULL,
  PRIMARY KEY(lists_edition_id, entity_edition_id),
  INDEX lists_edition_has_entity_edition_FKIndex1(lists_edition_id),
  INDEX lists_edition_has_entity_edition_FKIndex2(entity_edition_id),
  INDEX lists_edition_list_entity_edition_FKIndex3(edition_read_status_type_id),
  INDEX lists_edition_list_entity_edition_FKIndex4(condition_type_id),
  INDEX lists_edition_list_entity_edition_FKIndex5(ownership_status_id),
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
TYPE=InnoDB;

CREATE TABLE persona_affiliation (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  persona_id INTEGER UNSIGNED NOT NULL,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id),
  INDEX persona_affiliation_FKIndex1(persona_id),
  FOREIGN KEY(persona_id)
    REFERENCES persona(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE game_release (
  entity_release_id BIGINT UNSIGNED NOT NULL,
  emulate BOOL NOT NULL DEFAULT 0 AUTO_INCREMENT,
  installation_instructions TEXT NULL,
  PRIMARY KEY(entity_release_id),
  INDEX game_release_FKIndex1(entity_release_id),
  FOREIGN KEY(entity_release_id)
    REFERENCES entity_release(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE persona_race (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  persona_id INTEGER UNSIGNED NOT NULL,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id),
  INDEX Race_FKIndex1(persona_id),
  FOREIGN KEY(persona_id)
    REFERENCES persona(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE persona_unusual_features (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  persona_id INTEGER UNSIGNED NOT NULL,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id),
  INDEX persona_unusual_features_FKIndex1(persona_id),
  FOREIGN KEY(persona_id)
    REFERENCES persona(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE persona_occupation (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  persona_id INTEGER UNSIGNED NOT NULL,
  occupation VARCHAR NOT NULL,
  PRIMARY KEY(id),
  INDEX persona_occupation_FKIndex1(persona_id),
  FOREIGN KEY(persona_id)
    REFERENCES persona(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE soundtrack_for_entity_edition (
  soundtrack_id INTEGER UNSIGNED NOT NULL,
  entity_edition_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(soundtrack_id, entity_edition_id),
  INDEX soundtrack_has_entity_edition_FKIndex1(soundtrack_id),
  INDEX soundtrack_has_entity_edition_FKIndex2(entity_edition_id),
  FOREIGN KEY(soundtrack_id)
    REFERENCES soundtrack(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_edition_id)
    REFERENCES entity_edition(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE persona_appear_on_entity (
  persona_id INTEGER UNSIGNED NOT NULL,
  entity_id BIGINT UNSIGNED NOT NULL,
  first_appear BOOL NOT NULL,
  PRIMARY KEY(persona_id, entity_id),
  INDEX persona_has_entity_FKIndex1(persona_id),
  INDEX persona_has_entity_FKIndex2(entity_id),
  FOREIGN KEY(persona_id)
    REFERENCES persona(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_id)
    REFERENCES entity(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE persona_alias (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  alias_type_id INTEGER UNSIGNED NOT NULL,
  persona_id INTEGER UNSIGNED NOT NULL,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id),
  INDEX persona_associated_name_FKIndex1(persona_id),
  INDEX persona_alias_FKIndex2(alias_type_id),
  FOREIGN KEY(persona_id)
    REFERENCES persona(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(alias_type_id)
    REFERENCES alias_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE software_edition_has_subtitle (
  software_edition_entity_edition_id INTEGER UNSIGNED NOT NULL,
  language_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(software_edition_entity_edition_id, language_id),
  INDEX software_edition_has_language_FKIndex1(software_edition_entity_edition_id),
  INDEX software_edition_has_language_FKIndex2(language_id),
  FOREIGN KEY(software_edition_entity_edition_id)
    REFERENCES software_edition(entity_edition_id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(language_id)
    REFERENCES language(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE software_edition_has_version (
  software_edition_entity_edition_id INTEGER UNSIGNED NOT NULL,
  version_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(software_edition_entity_edition_id, version_id),
  INDEX software_edition_has_version_FKIndex1(software_edition_entity_edition_id),
  INDEX software_edition_has_version_FKIndex2(version_id),
  FOREIGN KEY(software_edition_entity_edition_id)
    REFERENCES software_edition(entity_edition_id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(version_id)
    REFERENCES version(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE read_edition (
  entity_edition_id INTEGER UNSIGNED NOT NULL,
  print_type_id INTEGER UNSIGNED NOT NULL,
  pages_number INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  chapters_number INTEGER UNSIGNED NULL,
  PRIMARY KEY(entity_edition_id),
  INDEX read_edition_FKIndex1(entity_edition_id),
  INDEX read_edition_FKIndex2(print_type_id),
  FOREIGN KEY(entity_edition_id)
    REFERENCES entity_edition(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(print_type_id)
    REFERENCES print_type(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
);

CREATE TABLE mod (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  entity_release_id BIGINT UNSIGNED NOT NULL,
  mod_type_id INTEGER UNSIGNED NOT NULL,
  name VARCHAR NOT NULL,
  author VARCHAR NOT NULL,
  launch_date DATE NULL,
  description TEXT NULL,
  installation_instruction TEXT NULL,
  PRIMARY KEY(id),
  INDEX mod_FKIndex2(mod_type_id),
  INDEX mod_FKIndex2(entity_release_id),
  FOREIGN KEY(mod_type_id)
    REFERENCES mod_type(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_release_id)
    REFERENCES entity_release(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE entity_release_comments (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  entity_release_id BIGINT UNSIGNED NOT NULL,
  users_id INTEGER UNSIGNED NOT NULL,
  content TEXT NOT NULL,
  title VARCHAR NOT NULL,
  create_date DATETIME NOT NULL,
  update_date DATETIME NOT NULL,
  PRIMARY KEY(id),
  INDEX comments_FKIndex1(users_id),
  INDEX comments_FKIndex2(entity_release_id),
  FOREIGN KEY(users_id)
    REFERENCES users(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_release_id)
    REFERENCES entity_release(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE entity_release_has_language (
  entity_release_id BIGINT UNSIGNED NOT NULL,
  language_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(entity_release_id, language_id),
  INDEX entity_release_has_language_FKIndex1(entity_release_id),
  INDEX entity_release_has_language_FKIndex2(language_id),
  FOREIGN KEY(entity_release_id)
    REFERENCES entity_release(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(language_id)
    REFERENCES language(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE entity_release_has_version (
  entity_release_id BIGINT UNSIGNED NOT NULL,
  version_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(entity_release_id, version_id),
  INDEX entity_release_has_version_FKIndex1(entity_release_id),
  INDEX entity_release_has_version_FKIndex2(version_id),
  FOREIGN KEY(entity_release_id)
    REFERENCES entity_release(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(version_id)
    REFERENCES version(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE entity_edition_comments (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  entity_edition_id INTEGER UNSIGNED NOT NULL,
  users_id INTEGER UNSIGNED NOT NULL,
  content TEXT NOT NULL,
  title VARCHAR NOT NULL,
  create_date DATETIME NOT NULL,
  update_date DATETIME NOT NULL,
  PRIMARY KEY(id),
  INDEX edition_comments_FKIndex1(users_id),
  INDEX entity_edition_comments_FKIndex2(entity_edition_id),
  FOREIGN KEY(users_id)
    REFERENCES users(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_edition_id)
    REFERENCES entity_edition(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE entity_edition_has_currency (
  entity_edition_id INTEGER UNSIGNED NOT NULL,
  currency_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(entity_edition_id, currency_id),
  INDEX entity_edition_has_currency_FKIndex1(entity_edition_id),
  INDEX entity_edition_has_currency_FKIndex2(currency_id),
  FOREIGN KEY(entity_edition_id)
    REFERENCES entity_edition(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(currency_id)
    REFERENCES currency(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE entity_edition_has_subtitle (
  language_id INTEGER UNSIGNED NOT NULL,
  entity_edition_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(language_id, entity_edition_id),
  INDEX language_has_entity_edition_FKIndex1(language_id),
  INDEX language_has_entity_edition_FKIndex2(entity_edition_id),
  FOREIGN KEY(language_id)
    REFERENCES language(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(entity_edition_id)
    REFERENCES entity_edition(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE entity_edition_has_language (
  entity_edition_id INTEGER UNSIGNED NOT NULL,
  language_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(entity_edition_id, language_id),
  INDEX entity_edition_has_language_FKIndex1(entity_edition_id),
  INDEX entity_edition_has_language_FKIndex2(language_id),
  FOREIGN KEY(entity_edition_id)
    REFERENCES entity_edition(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(language_id)
    REFERENCES language(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE number_edition (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  entity_edition_id INTEGER UNSIGNED NOT NULL,
  number_type_id INTEGER UNSIGNED NOT NULL,
  entity_type_id INTEGER UNSIGNED NOT NULL,
  number INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(id),
  INDEX number_edition_FKIndex1(entity_type_id),
  INDEX number_edition_FKIndex2(number_type_id),
  INDEX number_edition_FKIndex3(entity_edition_id),
  FOREIGN KEY(entity_type_id)
    REFERENCES entity_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(number_type_id)
    REFERENCES number_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_edition_id)
    REFERENCES entity_edition(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
);

CREATE TABLE number_release (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  number_release_id INTEGER UNSIGNED NOT NULL,
  entity_release_id BIGINT UNSIGNED NOT NULL,
  number_type_id INTEGER UNSIGNED NOT NULL,
  entity_type_id INTEGER UNSIGNED NOT NULL,
  number INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(id),
  INDEX number_release_FKIndex1(entity_type_id),
  INDEX number_release_FKIndex2(number_type_id),
  INDEX number_release_FKIndex3(entity_release_id),
  INDEX number_release_FKIndex4(number_release_id),
  FOREIGN KEY(entity_type_id)
    REFERENCES entity_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION,
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
TYPE=InnoDB;

CREATE TABLE collaborator_provides_release (
  collaborator_id INTEGER UNSIGNED NOT NULL,
  entity_release_id BIGINT UNSIGNED NOT NULL,
  collaborator_type_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(collaborator_id, entity_release_id),
  INDEX collaborator_has_entity_release_FKIndex1(collaborator_id),
  INDEX collaborator_has_entity_release_FKIndex2(entity_release_id),
  INDEX collaborator_provides_release_FKIndex3(collaborator_type_id),
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
TYPE=InnoDB;

CREATE TABLE company_has_entity_edition (
  company_id INTEGER UNSIGNED NOT NULL,
  entity_edition_id INTEGER UNSIGNED NOT NULL,
  company_function_type_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(company_id, entity_edition_id),
  INDEX company_has_entity_edition_FKIndex1(company_id),
  INDEX company_has_entity_edition_FKIndex2(entity_edition_id),
  INDEX company_has_entity_edition_FKIndex3(company_function_type_id),
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
TYPE=InnoDB;

CREATE TABLE entity_edition_launch_country (
  entity_edition_id INTEGER UNSIGNED NOT NULL,
  country_id INTEGER UNSIGNED NOT NULL,
  currency_id INTEGER UNSIGNED NOT NULL,
  launch_date DATETIME NOT NULL,
  launch_price DECIMAL NOT NULL,
  PRIMARY KEY(entity_edition_id, country_id),
  INDEX entity_edition_has_country_FKIndex1(entity_edition_id),
  INDEX entity_edition_has_country_FKIndex2(country_id),
  INDEX entity_edition_launch_country_FKIndex3(currency_id),
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
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE entity_edition_has_image (
  image_id BIGINT UNSIGNED NOT NULL,
  entity_edition_id INTEGER UNSIGNED NOT NULL,
  image_entity_edition_type_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(image_id, entity_edition_id),
  INDEX image_has_entity_edition_FKIndex1(image_id),
  INDEX image_has_entity_edition_FKIndex2(entity_edition_id),
  INDEX image_has_entity_edition_FKIndex3(image_entity_edition_type_id),
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
TYPE=InnoDB;

CREATE TABLE collaborator_member_produces_entity_release (
  collaborator_member_id INTEGER UNSIGNED NOT NULL,
  entity_release_id BIGINT UNSIGNED NOT NULL,
  function_type_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(collaborator_member_id, entity_release_id),
  INDEX member_has_entity_release_FKIndex1(collaborator_member_id),
  INDEX member_has_entity_release_FKIndex2(entity_release_id),
  INDEX member_produces_entity_release_FKIndex3(function_type_id),
  FOREIGN KEY(collaborator_member_id)
    REFERENCES collaborator_member(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(entity_release_id)
    REFERENCES entity_release(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(function_type_id)
    REFERENCES function_type(id)
      ON DELETE SET NULL
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE mod_has_image (
  mod_id INTEGER UNSIGNED NOT NULL,
  image_id BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY(mod_id, image_id),
  INDEX mod_has_image_FKIndex1(mod_id),
  INDEX mod_has_image_FKIndex2(image_id),
  FOREIGN KEY(mod_id)
    REFERENCES mod(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(image_id)
    REFERENCES image(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
)
TYPE=InnoDB;

CREATE TABLE people_voice_persona_on_number_edition (
  people_voice_persona_language_id INTEGER UNSIGNED NOT NULL,
  people_voice_persona_people_id BIGINT UNSIGNED NOT NULL,
  people_voice_persona_persona_id INTEGER UNSIGNED NOT NULL,
  number_edition_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(people_voice_persona_language_id, people_voice_persona_people_id, people_voice_persona_persona_id, number_edition_id),
  INDEX people_voice_persona_has_number_edition_FKIndex1(people_voice_persona_persona_id, people_voice_persona_people_id, people_voice_persona_language_id),
  INDEX people_voice_persona_has_number_edition_FKIndex2(number_edition_id),
  FOREIGN KEY(people_voice_persona_persona_id, people_voice_persona_people_id, people_voice_persona_language_id)
    REFERENCES people_voice_persona(persona_id, people_id, language_id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(number_edition_id)
    REFERENCES number_edition(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
);


