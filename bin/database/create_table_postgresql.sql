CREATE DATABASE crawler
 WITH ENCODING='UTF8'
    OWNER=postgres
    CONNECTION LIMIT=-1;
	  

CREATE TABLE IF NOT EXISTS function_type (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS genre_type (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS related_type (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS filter_type (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS image (
 id SERIAL NOT NULL,
 url VARCHAR NOT NULL,
 extension VARCHAR NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS image_edition_type (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS read_status_type (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS hash_type (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS figure_version (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS shops (
 id SERIAL NOT NULL,
 url VARCHAR NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS scale (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS social_type (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 website VARCHAR NULL,
 website_secure VARCHAR NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS shop_location (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS release_read_status_type (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS release_ownership_type (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS entity_type (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS release_type (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS material (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS media_type (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TYPE gender AS ENUM ('Female', 'Male', 'Undefined');

CREATE TABLE IF NOT EXISTS users (
 id SERIAL NOT NULL,
 username VARCHAR UNIQUE NOT NULL,
 pass VARCHAR NOT NULL,
 user_gender gender NOT NULL,
 location VARCHAR NOT NULL,
 birthday DATE NOT NULL,
 signup_date timestamp without time zone NOT NULL,
 activated BOOLEAN NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS lyric_type (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS number_type (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS ownership_status (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS member (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 active BOOLEAN NOT NULL DEFAULT '1',
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS mod_type (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS plataform_type (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS production_type (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS produces_type (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS image_figure_type (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS product_condition_type (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS produces_figure_type (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS print_type (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS image_soundtrack_type (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS language (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 code VARCHAR NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS stage_developer_type (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS source (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 url_base VARCHAR NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS collaborator_type (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS collection (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 description TEXT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS compose_type (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS condition_type (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS company_function_type (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS soundtrack_type (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS blood_type (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS box_condition_type (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS audio_codec (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS based_type (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS collaborator (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 irc VARCHAR NULL,
 description TEXT NULL,
 create_date timestamp without time zone NOT NULL DEFAULT clock_timestamp(),
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS tag (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS category (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS classification_type (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS edition_type (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS currency (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 symbol VARCHAR NULL,
 code VARCHAR NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS country (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 code VARCHAR NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS software_type (
 id SERIAL NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS social (
 id SERIAL NOT NULL,
 social_type_id INTEGER NOT NULL,
 url VARCHAR NOT NULL,
 PRIMARY KEY(id)
);

ALTER TABLE social ADD CONSTRAINT social_type_id FOREIGN KEY(social_type_id) REFERENCES social_type(id) ON DELETE NO ACTION ON UPDATE NO ACTION;

CREATE TABLE IF NOT EXISTS lists_figure (
 id SERIAL NOT NULL,
 user_id INTEGER NOT NULL,
 name VARCHAR NOT NULL,
 create_date timestamp without time zone NULL,
 PRIMARY KEY(id),
 FOREIGN KEY(user_id)
  REFERENCES users(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);



CREATE TABLE IF NOT EXISTS urls (
 source_id SERIAL NOT NULL,
 link VARCHAR NOT NULL,
 last_checked timestamp without time zone NULL,
 PRIMARY KEY(source_id, link),
 FOREIGN KEY(source_id)
  REFERENCES source(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION
);


CREATE TABLE IF NOT EXISTS version (
 id SERIAL NOT NULL,
 stage_developer_type_id INTEGER NOT NULL,
 number VARCHAR NULL,
 changelog TEXT NULL,
 PRIMARY KEY(id),
 FOREIGN KEY(stage_developer_type_id)
  REFERENCES stage_developer_type(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS collaborator_website (
 collaborator_id INTEGER NOT NULL,
 website VARCHAR NOT NULL,
 PRIMARY KEY(collaborator_id, website),
 FOREIGN KEY(collaborator_id)
  REFERENCES collaborator(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS event (
 id SERIAL NOT NULL,
 currency_id INTEGER NOT NULL,
 name VARCHAR NOT NULL,
 location VARCHAR NULL,
 website VARCHAR NULL,
 date DATE NULL,
 duration INTEGER NULL,
 PRIMARY KEY(id),
 FOREIGN KEY(currency_id)
  REFERENCES currency(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS company (
 id SERIAL NOT NULL,
 country_id INTEGER NOT NULL,
 name VARCHAR NOT NULL,
 social_name VARCHAR NOT NULL,
 start_year CHAR(4) NULL,
 website VARCHAR NULL,
 description TEXT NULL,
 create_date timestamp without time zone NULL,
 PRIMARY KEY(id),
 FOREIGN KEY(country_id)
  REFERENCES country(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS user_email (
 user_id INTEGER NOT NULL,
 email VARCHAR NULL,
 FOREIGN KEY(user_id)
  REFERENCES users(id)
   ON DELETE CASCADE
   ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS soundtrack (
 id SERIAL NOT NULL,
 soundtrack_type_id INTEGER NOT NULL,
 name VARCHAR NOT NULL,
 launch_year CHAR(4) NULL,
 PRIMARY KEY(id),
 FOREIGN KEY(soundtrack_type_id)
  REFERENCES soundtrack_type(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS requirements (
 id SERIAL NOT NULL,
 version_id INTEGER NOT NULL,
 video_board VARCHAR NULL,
 processor VARCHAR NULL,
 memory VARCHAR NULL,
 hd_storage VARCHAR NULL,
 PRIMARY KEY(id),
 FOREIGN KEY(version_id)
  REFERENCES version(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS driver (
 id SERIAL NOT NULL,
 requirements_id INTEGER NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id),
 FOREIGN KEY(requirements_id)
  REFERENCES requirements(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS people (
 id SERIAL NOT NULL,
 country_id INTEGER NOT NULL,
 blood_type_id INTEGER NOT NULL,
 name VARCHAR NOT NULL,
 last_name VARCHAR NOT NULL,
 website VARCHAR NULL,
 description TEXT NULL,
 PRIMARY KEY(id),
 FOREIGN KEY(blood_type_id)
  REFERENCES blood_type(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION,
 FOREIGN KEY(country_id)
  REFERENCES country(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS people_nacionalization (
 people_id INTEGER NOT NULL,
 country_id INTEGER NOT NULL,
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

CREATE TABLE IF NOT EXISTS collaborator_has_social (
 social_id INTEGER NOT NULL,
 collaborator_id INTEGER NOT NULL,
 create_date timestamp without time zone NULL,
 last_checked timestamp without time zone NULL,
 PRIMARY KEY(social_id, collaborator_id),
 FOREIGN KEY(social_id)
  REFERENCES social(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(collaborator_id)
  REFERENCES collaborator(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS shops_operate_on_country (
 shops_id INTEGER NOT NULL,
 country_id INTEGER NOT NULL,
 PRIMARY KEY(shops_id, country_id),
 FOREIGN KEY(shops_id)
  REFERENCES shops(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(country_id)
  REFERENCES country(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS company_has_social (
 social_id INTEGER NOT NULL,
 company_id INTEGER NOT NULL,
 last_checked timestamp without time zone NULL,
 create_date timestamp without time zone NULL,
 PRIMARY KEY(social_id, company_id),
 FOREIGN KEY(social_id)
  REFERENCES social(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(company_id)
  REFERENCES company(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS people_has_social (
 social_id INTEGER NOT NULL,
 people_id INTEGER NOT NULL,
 last_checked timestamp without time zone NULL,
 create_date timestamp without time zone NULL,
 PRIMARY KEY(social_id, people_id),
 FOREIGN KEY(social_id)
  REFERENCES social(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(people_id)
  REFERENCES people(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS collaborator_has_member (
 collaborator_id INTEGER NOT NULL,
 member_id INTEGER NOT NULL,
 founder BOOLEAN NOT NULL,
 PRIMARY KEY(collaborator_id, member_id),
 FOREIGN KEY(collaborator_id)
  REFERENCES collaborator(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(member_id)
  REFERENCES member(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS soundtrack_integrate_collection (
 collection_id INTEGER NOT NULL,
 soundtrack_id INTEGER NOT NULL,
 PRIMARY KEY(collection_id, soundtrack_id),
 FOREIGN KEY(collection_id)
  REFERENCES collection(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(soundtrack_id)
  REFERENCES soundtrack(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS audio (
 id SERIAL NOT NULL,
 country_id INTEGER NOT NULL,
 audio_codec_id INTEGER NOT NULL,
 name VARCHAR NOT NULL,
 duration TIME NULL,
 bitrate INTEGER NULL,
 PRIMARY KEY(id),
 FOREIGN KEY(audio_codec_id)
  REFERENCES audio_codec(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION,
 FOREIGN KEY(country_id)
  REFERENCES country(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS audio_has_language (
 audio_id INTEGER NOT NULL,
 language_id INTEGER NOT NULL,
 PRIMARY KEY(audio_id, language_id),
 FOREIGN KEY(audio_id)
  REFERENCES audio(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(language_id)
  REFERENCES language(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS company_has_country (
 country_id INTEGER NOT NULL,
 company_id INTEGER NOT NULL,
 PRIMARY KEY(country_id, company_id),
 FOREIGN KEY(country_id)
  REFERENCES country(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION,
 FOREIGN KEY(company_id)
  REFERENCES company(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS country_has_currency (
 currency_id INTEGER NOT NULL,
 country_id INTEGER NOT NULL,
 main BOOLEAN NOT NULL,
 PRIMARY KEY(currency_id, country_id),
 FOREIGN KEY(currency_id)
  REFERENCES currency(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION,
 FOREIGN KEY(country_id)
  REFERENCES country(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION
);

CREATE TABLE tag_has_filter_type (
  user_filter_type_id INTEGER NOT NULL,
  tag_id INTEGER NOT NULL,
  PRIMARY KEY(user_filter_type_id, tag_id),
  FOREIGN KEY(user_filter_type_id)
    REFERENCES filter_type(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(tag_id)
    REFERENCES tag(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS company_sponsors_event (
 company_id INTEGER NOT NULL,
 event_id INTEGER NOT NULL,
 PRIMARY KEY(company_id, event_id),
 FOREIGN KEY(company_id)
  REFERENCES company(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION,
 FOREIGN KEY(event_id)
  REFERENCES event(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS company_owner_collection (
 company_id INTEGER NOT NULL,
 collection_id INTEGER NOT NULL,
 PRIMARY KEY(company_id, collection_id),
 FOREIGN KEY(company_id)
  REFERENCES company(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(collection_id)
  REFERENCES collection(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS user_filter (
 id SERIAL NOT NULL,
 filter_type_id INTEGER NOT NULL,
 user_id INTEGER NOT NULL,
 dont_show_content VARCHAR NULL,
 PRIMARY KEY(id),
 FOREIGN KEY(user_id)
  REFERENCES users(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(filter_type_id)
  REFERENCES filter_type(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION
);

CREATE TABLE category_has_filter_type (
  category_id INTEGER NOT NULL,
  filter_type_id INTEGER NOT NULL,
  PRIMARY KEY(category_id, filter_type_id),
  FOREIGN KEY(category_id)
    REFERENCES category(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY(filter_type_id)
    REFERENCES filter_type(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS lists_edition (
 id SERIAL NOT NULL,
 entity_type_id INTEGER NOT NULL,
 user_id INTEGER NOT NULL,
 name VARCHAR NOT NULL,
 create_date timestamp without time zone NULL,
 PRIMARY KEY(id),
 FOREIGN KEY(user_id)
  REFERENCES users(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(entity_type_id)
  REFERENCES entity_type(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS lists_release (
 id SERIAL NOT NULL,
 entity_type_id INTEGER NOT NULL,
 user_id INTEGER NOT NULL,
 name VARCHAR NOT NULL,
 create_date timestamp without time zone NULL,
 PRIMARY KEY(id),
 FOREIGN KEY(user_id)
  REFERENCES users(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(entity_type_id)
  REFERENCES entity_type(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS users_has_social (
 user_id INTEGER NOT NULL,
 social_id INTEGER NOT NULL,
 last_checked timestamp without time zone NULL,
 create_date timestamp without time zone NULL,
 PRIMARY KEY(user_id, social_id),
 FOREIGN KEY(user_id)
  REFERENCES users(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(social_id)
  REFERENCES social(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS country_has_language (
 language_id INTEGER NOT NULL,
 country_id INTEGER NOT NULL,
 PRIMARY KEY(language_id, country_id),
 FOREIGN KEY(language_id)
  REFERENCES language(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(country_id)
  REFERENCES country(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS genre_type_has_audio (
 genre_type_id INTEGER NOT NULL,
 audio_id INTEGER NOT NULL,
 PRIMARY KEY(genre_type_id, audio_id),
 FOREIGN KEY(genre_type_id)
  REFERENCES genre_type(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(audio_id)
  REFERENCES audio(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS people_has_image (
 image_id INTEGER NOT NULL,
 people_id INTEGER NOT NULL,
 PRIMARY KEY(image_id, people_id),
 FOREIGN KEY(image_id)
  REFERENCES image(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(people_id)
  REFERENCES people(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS soundtrack_has_image (
 soundtrack_id INTEGER NOT NULL,
 image_id INTEGER NOT NULL,
 image_soundtrack_type_id INTEGER NOT NULL,
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
   ON DELETE NO ACTION
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS people_compose_audio (
 audio_id INTEGER NOT NULL,
 people_id INTEGER NOT NULL,
 compose_type_id INTEGER NOT NULL,
 PRIMARY KEY(audio_id, people_id),
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
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS lyrics (
 id SERIAL NOT NULL,
 lyric_type_id INTEGER NOT NULL,
 user_id INTEGER NOT NULL,
 audio_id INTEGER NOT NULL,
 language_id INTEGER NOT NULL,
 lyric TEXT NULL,
 PRIMARY KEY(id),
 FOREIGN KEY(language_id)
  REFERENCES language(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION,
 FOREIGN KEY(audio_id)
  REFERENCES audio(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(user_id)
  REFERENCES users(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION,
 FOREIGN KEY(lyric_type_id)
  REFERENCES lyric_type(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS entity (
 id SERIAL NOT NULL,
 entity_type_id INTEGER NOT NULL,
 classification_type_id INTEGER NOT NULL,
 collection_id INTEGER NOT NULL,
 language_id INTEGER NOT NULL,
 country_id INTEGER NOT NULL,
 title VARCHAR NULL,
 romanized_title VARCHAR NULL,
 subtitle VARCHAR NULL,
 synopse TEXT NULL,
 launch_year CHAR(4) NULL,
 collection_started BOOLEAN NULL,
 PRIMARY KEY(id),
 FOREIGN KEY(country_id)
  REFERENCES country(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION,
 FOREIGN KEY(language_id)
  REFERENCES language(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION,
 FOREIGN KEY(collection_id)
  REFERENCES collection(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION,
 FOREIGN KEY(classification_type_id)
  REFERENCES classification_type(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION,
 FOREIGN KEY(entity_type_id)
  REFERENCES entity_type(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS archive (
 id SERIAL NOT NULL,
 version_id INTEGER NOT NULL,
 name VARCHAR NOT NULL,
 url VARCHAR NULL,
 size INTEGER NULL,
 extension VARCHAR NULL,
 PRIMARY KEY(id),
 FOREIGN KEY(version_id)
  REFERENCES version(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS alias (
 id SERIAL NOT NULL,
 people_id INTEGER NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id),
 FOREIGN KEY(people_id)
  REFERENCES people(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS entity_associated_name (
 id SERIAL NOT NULL,
 entity_id INTEGER NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id),
 FOREIGN KEY(entity_id)
  REFERENCES entity(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS persona (
 id SERIAL NOT NULL,
 blood_type_id INTEGER NOT NULL,
 entity_id INTEGER NOT NULL,
 name VARCHAR NOT NULL,
 personage_gender gender NULL,
 first_appear_on VARCHAR NULL,
 height INTEGER NULL,
 weight DECIMAL NULL,
 eyes_color VARCHAR NULL,
 hair_color VARCHAR NULL,
 PRIMARY KEY(id),
 FOREIGN KEY(entity_id)
  REFERENCES entity(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION,
 FOREIGN KEY(blood_type_id)
  REFERENCES blood_type(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS soundtrack_has_audio (
 soundtrack_id INTEGER NOT NULL,
 audio_id INTEGER NOT NULL,
 exclusive BOOLEAN NULL,
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

CREATE TABLE IF NOT EXISTS entity_has_tag (
 tag_id INTEGER NOT NULL,
 entity_id INTEGER NOT NULL,
 PRIMARY KEY(tag_id, entity_id),
 FOREIGN KEY(tag_id)
  REFERENCES tag(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(entity_id)
  REFERENCES entity(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS entity_has_category (
 entity_id INTEGER NOT NULL,
 category_id INTEGER NOT NULL,
 PRIMARY KEY(entity_id, category_id),
 FOREIGN KEY(entity_id)
  REFERENCES entity(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(category_id)
  REFERENCES category(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS hash (
 id SERIAL NOT NULL,
 hash_type_id INTEGER NOT NULL,
 archive_id INTEGER NOT NULL,
 code TEXT NULL,
 create_date timestamp without time zone NULL,
 PRIMARY KEY(id),
 FOREIGN KEY(archive_id)
  REFERENCES archive(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(hash_type_id)
  REFERENCES hash_type(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS people_produces_entity (
 people_id INTEGER NOT NULL,
 entity_id INTEGER NOT NULL,
 production_type_id INTEGER NOT NULL,
 PRIMARY KEY(people_id, entity_id),
 FOREIGN KEY(people_id)
  REFERENCES people(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(entity_id)
  REFERENCES entity(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(production_type_id)
  REFERENCES production_type(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS entity_has_entity (
 entity_id INTEGER NOT NULL,
 other_entity_id INTEGER NOT NULL,
 based_type_id INTEGER NOT NULL,
 PRIMARY KEY(entity_id,other_entity_id),
 FOREIGN KEY(entity_id)
  REFERENCES entity(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION,
 FOREIGN KEY(other_entity_id)
  REFERENCES entity(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION,
 FOREIGN KEY(based_type_id)
  REFERENCES based_type(id)
   ON DELETE SET DEFAULT
   ON UPDATE NO ACTION
);







CREATE TABLE IF NOT EXISTS persona_related_persona (
 persona_id INTEGER NOT NULL,
 other_persona_id INTEGER NOT NULL,
 related_type_id INTEGER NOT NULL,
 PRIMARY KEY(persona_id,other_persona_id),
 FOREIGN KEY(other_persona_id)
  REFERENCES persona(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(persona_id)
  REFERENCES persona(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(related_type_id)
  REFERENCES related_type(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS entity_edition (
 id SERIAL NOT NULL,
 edition_type_id INTEGER NOT NULL,
 event_id INTEGER NOT NULL,
 entity_id INTEGER NOT NULL,
 title VARCHAR NOT NULL,
 free BOOLEAN NOT NULL,
 release_description TEXT NULL,
 censored BOOLEAN NULL,
 code VARCHAR NULL,
 complement_code VARCHAR NULL,
 height INTEGER NULL,
 width INTEGER NULL,
 depth INTEGER NULL,
 weight DECIMAL NULL,
 PRIMARY KEY(id),
 FOREIGN KEY(entity_id)
  REFERENCES entity(id)
   ON DELETE CASCADE
   ON UPDATE CASCADE,
 FOREIGN KEY(event_id)
  REFERENCES event(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION,
 FOREIGN KEY(edition_type_id)
  REFERENCES edition_type(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION
  
);

CREATE TABLE IF NOT EXISTS software_edition (
 entity_edition_id INTEGER NOT NULL,
 plataform_type_id INTEGER NOT NULL,
 software_type_id INTEGER NOT NULL,
 media_type_id INTEGER NOT NULL,
 PRIMARY KEY(entity_edition_id),
 FOREIGN KEY(entity_edition_id)
  REFERENCES entity_edition(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(media_type_id)
  REFERENCES media_type(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION,
 FOREIGN KEY(software_type_id)
  REFERENCES software_type(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION,
 FOREIGN KEY(plataform_type_id)
  REFERENCES plataform_type(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS entity_release (
 id SERIAL NOT NULL,
 entity_id INTEGER NOT NULL,
 release_type_id INTEGER NOT NULL,
 country_id INTEGER NOT NULL,
 entity_edition_id INTEGER NOT NULL,
 description TEXT NULL,
 release_date timestamp without time zone NULL,
 PRIMARY KEY(id),
 FOREIGN KEY(entity_edition_id)
  REFERENCES entity_edition(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(country_id)
  REFERENCES country(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION,
 FOREIGN KEY(release_type_id)
  REFERENCES release_type(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION,
 FOREIGN KEY(entity_id)
  REFERENCES entity(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS lists_release_list_entity_release (
 lists_release_id INTEGER NOT NULL,
 entity_release_id INTEGER NOT NULL,
 release_read_status_type_id INTEGER NOT NULL,
 release_ownership_type_id INTEGER NOT NULL,
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
   ON DELETE NO ACTION
   ON UPDATE NO ACTION,
 FOREIGN KEY(release_read_status_type_id)
  REFERENCES release_read_status_type(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS figure (
 id SERIAL NOT NULL,
 entity_id INTEGER NOT NULL,
 figure_version_id INTEGER NOT NULL,
 currency_id INTEGER NOT NULL,
 scale_id INTEGER NOT NULL,
 country_id INTEGER NOT NULL,
 height SMALLINT  NULL,
 width SMALLINT  NULL,
 weight DECIMAL NULL,
 launch_price DECIMAL NULL,
 release_date DATE NULL,
 observation TEXT NOT NULL,
 PRIMARY KEY(id),
 FOREIGN KEY(country_id)
  REFERENCES country(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION,
 FOREIGN KEY(scale_id)
  REFERENCES scale(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION,
 FOREIGN KEY(currency_id)
  REFERENCES currency(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION,
 FOREIGN KEY(figure_version_id)
  REFERENCES figure_version(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION,
 FOREIGN KEY(entity_id)
  REFERENCES entity(id)
   ON DELETE NO ACTION
   ON UPDATE SET NULL
);

CREATE TABLE IF NOT EXISTS lists_figure_list_figure (
 lists_figure_id INTEGER NOT NULL,
 figure_id INTEGER NOT NULL,
 ownership_status_id INTEGER NOT NULL,
 box_condition_type_id INTEGER NOT NULL,
 product_condition_type_id INTEGER NOT NULL,
 observation TEXT NULL,
 PRIMARY KEY(lists_figure_id, figure_id),
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
   ON DELETE NO ACTION
   ON UPDATE NO ACTION,
 FOREIGN KEY(box_condition_type_id)
  REFERENCES box_condition_type(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION,
 FOREIGN KEY(ownership_status_id)
  REFERENCES ownership_status(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS lists_edition_list_entity_edition (
 lists_edition_id INTEGER NOT NULL,
 entity_edition_id INTEGER NOT NULL,
 ownership_status_id INTEGER NOT NULL,
 condition_type_id INTEGER NOT NULL,
 read_status_type_id INTEGER NOT NULL,
 PRIMARY KEY(lists_edition_id, entity_edition_id),
 FOREIGN KEY(lists_edition_id)
  REFERENCES lists_edition(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(entity_edition_id)
  REFERENCES entity_edition(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(read_status_type_id)
  REFERENCES read_status_type(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION,
 FOREIGN KEY(condition_type_id)
  REFERENCES condition_type(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION,
 FOREIGN KEY(ownership_status_id)
  REFERENCES ownership_status(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS persona_race (
 id SERIAL NOT NULL,
 persona_id INTEGER NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id),
 FOREIGN KEY(persona_id)
  REFERENCES persona(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS persona_occupation (
 id SERIAL NOT NULL,
 persona_id INTEGER NOT NULL,
 occupation VARCHAR NULL,
 PRIMARY KEY(id),
 FOREIGN KEY(persona_id)
  REFERENCES persona(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS persona_unusual_features (
 id SERIAL NOT NULL,
 persona_id INTEGER NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id),
 FOREIGN KEY(persona_id)
  REFERENCES persona(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS persona_affiliation (
 id SERIAL NOT NULL,
 persona_id INTEGER NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id),
 FOREIGN KEY(persona_id)
  REFERENCES persona(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS persona_associated_name (
 id SERIAL NOT NULL,
 persona_id INTEGER NOT NULL,
 name VARCHAR NOT NULL,
 PRIMARY KEY(id),
 FOREIGN KEY(persona_id)
  REFERENCES persona(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS game_release (
 entity_release_id INTEGER NOT NULL,
 emulate BOOLEAN NOT NULL,
 installation_instructions TEXT NULL,
 PRIMARY KEY(entity_release_id),
 FOREIGN KEY(entity_release_id)
  REFERENCES entity_release(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS soundtrack_for_entity_edition (
 soundtrack_id INTEGER NOT NULL,
 entity_edition_id INTEGER NOT NULL,
 PRIMARY KEY(soundtrack_id, entity_edition_id),
 FOREIGN KEY(soundtrack_id)
  REFERENCES soundtrack(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(entity_edition_id)
  REFERENCES entity_edition(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS software_subtitle (
 software_edition_entity_edition_id INTEGER NOT NULL,
 language_id INTEGER NOT NULL,
 PRIMARY KEY(software_edition_entity_edition_id, language_id),
 FOREIGN KEY(software_edition_entity_edition_id)
  REFERENCES software_edition(entity_edition_id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(language_id)
  REFERENCES language(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS read_edition (
 entity_edition_id INTEGER NOT NULL,
 print_type_id INTEGER NOT NULL,
 pages_number SERIAL NOT NULL,
 chapters_number INTEGER NULL,
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

CREATE TABLE IF NOT EXISTS figure_has_tag (
 tag_id INTEGER NOT NULL,
 figure_id INTEGER NOT NULL,
 PRIMARY KEY(tag_id, figure_id),
 FOREIGN KEY(tag_id)
  REFERENCES tag(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(figure_id)
  REFERENCES figure(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE entity_edition_subtitle (
  language_id INTEGER  NOT NULL,
  entity_edition_id INTEGER  NOT NULL,
  PRIMARY KEY(language_id, entity_edition_id),
  FOREIGN KEY(language_id)
    REFERENCES language(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(entity_edition_id)
    REFERENCES entity_edition(id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS software_edition_has_version (
 software_edition_entity_edition_id INTEGER NOT NULL,
 version_id INTEGER NOT NULL,
 PRIMARY KEY(software_edition_entity_edition_id, version_id),
 FOREIGN KEY(software_edition_entity_edition_id)
  REFERENCES software_edition(entity_edition_id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(version_id)
  REFERENCES version(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS entity_release_has_language (
 entity_release_id INTEGER NOT NULL,
 language_id INTEGER NOT NULL,
 PRIMARY KEY(entity_release_id, language_id),
 FOREIGN KEY(entity_release_id)
  REFERENCES entity_release(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(language_id)
  REFERENCES language(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS entity_edition_launch_country (
 entity_edition_id INTEGER NOT NULL,
 country_id INTEGER NOT NULL,
 launch_date timestamp without time zone NULL,
 launch_price DECIMAL NULL,
 PRIMARY KEY(entity_edition_id, country_id),
 FOREIGN KEY(entity_edition_id)
  REFERENCES entity_edition(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(country_id)
  REFERENCES country(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS entity_edition_has_currency (
 entity_edition_id INTEGER NOT NULL,
 currency_id INTEGER NOT NULL,
 PRIMARY KEY(entity_edition_id, currency_id),
 FOREIGN KEY(entity_edition_id)
  REFERENCES entity_edition(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION,
 FOREIGN KEY(currency_id)
  REFERENCES currency(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS entity_edition_has_language (
 entity_edition_id INTEGER NOT NULL,
 language_id INTEGER NOT NULL,
 PRIMARY KEY(entity_edition_id, language_id),
 FOREIGN KEY(entity_edition_id)
  REFERENCES entity_edition(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(language_id)
  REFERENCES language(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS figure_has_shops (
 figure_id INTEGER NOT NULL,
 shops_id INTEGER NOT NULL,
 product_url VARCHAR NULL,
 checked_last timestamp without time zone NULL,
 PRIMARY KEY(figure_id, shops_id),
 FOREIGN KEY(figure_id)
  REFERENCES figure(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(shops_id)
  REFERENCES shops(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS figure_has_shop_location (
 figure_id INTEGER NOT NULL,
 shop_location_id INTEGER NOT NULL,
 PRIMARY KEY(figure_id, shop_location_id),
 FOREIGN KEY(figure_id)
  REFERENCES figure(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(shop_location_id)
  REFERENCES shop_location(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS figure_has_material (
 figure_id INTEGER NOT NULL,
 material_id INTEGER NOT NULL,
 PRIMARY KEY(figure_id, material_id),
 FOREIGN KEY(figure_id)
  REFERENCES figure(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(material_id)
  REFERENCES material(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS entity_release_has_version (
 entity_release_id INTEGER NOT NULL,
 version_id INTEGER NOT NULL,
 PRIMARY KEY(entity_release_id, version_id),
 FOREIGN KEY(entity_release_id)
  REFERENCES entity_release(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(version_id)
  REFERENCES version(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS figure_from_persona (
 figure_id INTEGER NOT NULL,
 persona_id INTEGER NOT NULL,
 PRIMARY KEY(figure_id, persona_id),
 FOREIGN KEY(figure_id)
  REFERENCES figure(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(persona_id)
  REFERENCES persona(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS category_has_figure (
 category_id INTEGER NOT NULL,
 figure_id INTEGER NOT NULL,
 PRIMARY KEY(category_id, figure_id),
 FOREIGN KEY(category_id)
  REFERENCES category(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(figure_id)
  REFERENCES figure(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS comments (
 id SERIAL NOT NULL,
 entity_release_id INTEGER NOT NULL,
 user_id INTEGER NOT NULL,
 content TEXT NULL,
 title VARCHAR NULL,
 create_date timestamp without time zone NULL,
 PRIMARY KEY(id),
 FOREIGN KEY(user_id)
  REFERENCES users(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(entity_release_id)
  REFERENCES entity_release(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS mod (
 id SERIAL NOT NULL,
 entity_release_id INTEGER NOT NULL,
 mod_type_id INTEGER NOT NULL,
 name VARCHAR NOT NULL,
 author VARCHAR NULL,
 launch_date DATE NULL,
 version VARCHAR NULL,
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
);

CREATE TABLE IF NOT EXISTS mod_has_image (
 mod_id INTEGER NOT NULL,
 image_id INTEGER NOT NULL,
 PRIMARY KEY(mod_id, image_id),
 FOREIGN KEY(mod_id)
  REFERENCES mod(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(image_id)
  REFERENCES image(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS company_produces_figure (
 company_id INTEGER NOT NULL,
 figure_id INTEGER NOT NULL,
 produces_figure_type_id INTEGER NOT NULL,
 PRIMARY KEY(company_id, figure_id),
 FOREIGN KEY(company_id)
  REFERENCES company(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(figure_id)
  REFERENCES figure(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(produces_figure_type_id)
  REFERENCES produces_figure_type(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS member_produces_entity_release (
 member_id INTEGER NOT NULL,
 entity_release_id INTEGER NOT NULL,
 function_type_id INTEGER NOT NULL,
 PRIMARY KEY(member_id, entity_release_id),
 FOREIGN KEY(member_id)
  REFERENCES member(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(entity_release_id)
  REFERENCES entity_release(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(function_type_id)
  REFERENCES function_type(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS collaborator_provides_release (
 collaborator_id INTEGER NOT NULL,
 entity_release_id INTEGER NOT NULL,
 collaborator_type_id INTEGER NOT NULL,
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
   ON DELETE NO ACTION
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS people_produces_figure (
 people_id INTEGER NOT NULL,
 figure_id INTEGER NOT NULL,
 produces_type_id INTEGER NOT NULL,
 PRIMARY KEY(people_id, figure_id),
 FOREIGN KEY(people_id)
  REFERENCES people(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(figure_id)
  REFERENCES figure(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(produces_type_id)
  REFERENCES produces_type(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS company_has_entity_edition (
 company_id INTEGER NOT NULL,
 entity_edition_id INTEGER NOT NULL,
 company_function_type_id INTEGER NOT NULL,
 PRIMARY KEY(company_id, entity_edition_id),
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
);

CREATE TABLE IF NOT EXISTS number_release (
 id SERIAL NOT NULL,
 entity_release_id INTEGER NOT NULL,
 number_type_id INTEGER NOT NULL,
 entity_type_id INTEGER NOT NULL,
 number INTEGER NULL,
 PRIMARY KEY(id),
 FOREIGN KEY(entity_type_id)
  REFERENCES entity_type(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION,
 FOREIGN KEY(number_type_id)
  REFERENCES number_type(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION,
 FOREIGN KEY(entity_release_id)
  REFERENCES entity_release(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS entity_edition_has_image (
 image_id INTEGER NOT NULL,
 entity_edition_id INTEGER NOT NULL,
 image_edition_type_id INTEGER NOT NULL,
 PRIMARY KEY(image_id, entity_edition_id),
 FOREIGN KEY(image_id)
  REFERENCES image(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(entity_edition_id)
  REFERENCES entity_edition(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION,
 FOREIGN KEY(image_edition_type_id)
  REFERENCES image_edition_type(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS figure_has_image (
 image_id INTEGER NOT NULL,
 figure_id INTEGER NOT NULL,
 image_figure_type_id INTEGER NOT NULL,
 PRIMARY KEY(image_id, figure_id),
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
   ON DELETE NO ACTION
   ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS number_edition (
 id SERIAL NOT NULL,
 entity_edition_id INTEGER NOT NULL,
 number_type_id INTEGER NOT NULL,
 entity_type_id INTEGER NOT NULL,
 number INTEGER NULL,
 PRIMARY KEY(id),
 FOREIGN KEY(entity_type_id)
  REFERENCES entity_type(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION,
 FOREIGN KEY(number_type_id)
  REFERENCES number_type(id)
   ON DELETE NO ACTION
   ON UPDATE NO ACTION,
 FOREIGN KEY(entity_edition_id)
  REFERENCES entity_edition(id)
   ON DELETE CASCADE
   ON UPDATE NO ACTION
);


