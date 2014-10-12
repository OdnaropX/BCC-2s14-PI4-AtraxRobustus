INSERT INTO function_type ( id, name) VALUES ();

INSERT INTO genre_type ( id, name) VALUES ();
INSERT INTO related_type ( id, name) VALUES ();
INSERT INTO filter_type ( id, name) VALUES ();
INSERT INTO image ( id, url, extension, name) VALUES ();
INSERT INTO image_edition_type (
 id,
 name
) VALUES ();
INSERT INTO read_status_type (
 id,
 name
) VALUES ();
INSERT INTO hash_type (
 id,
 name
) VALUES ();
INSERT INTO figure_version (
 id,
 name
) VALUES ();
INSERT INTO shops (
 id,
 url,
 name
) VALUES ();
INSERT INTO scale (
 id,
 name
) VALUES ();
INSERT INTO social_type (
 id,
 name,
 website ,
 website_secure
) VALUES ();
INSERT INTO shop_location (
 id,
 name
) VALUES ();
INSERT INTO release_read_status_type (
 id,
 name
) VALUES ();
INSERT INTO release_ownership_type (
 id,
 name
) VALUES ();
INSERT INTO entity_type (
 id,
 name
) VALUES ();
INSERT INTO release_type (
 id,
 name
) VALUES ();
INSERT INTO material (
 id,
 name
) VALUES ();
INSERT INTO media_type (
 id,
 name
) VALUES ();
INSERT INTO users (
 id,
 username ,
 pass,
 user_gender gender,
 location,
 birthday,
 signup_date,
 activated
) VALUES ();
INSERT INTO lyric_type (
 id,
 name,
) VALUES ();
INSERT INTO number_type (
 id,
 name,
) VALUES ();
INSERT INTO ownership_status (
 id,
 name,
) VALUES ();
INSERT INTO member (
 id,
 name,
 active
) VALUES ();
INSERT INTO mod_type (
 id,
 name,
) VALUES ();
INSERT INTO plataform_type (
 id,
 name,
) VALUES ();
INSERT INTO production_type (
 id,
 name,
) VALUES ();
INSERT INTO produces_type (
 id,
 name,
) VALUES ();
INSERT INTO image_figure_type (
 id,
 name,
) VALUES ();
INSERT INTO product_condition_type (
 id,
 name,
) VALUES ();
INSERT INTO produces_figure_type (
 id,
 name,
) VALUES ();
INSERT INTO print_type (
 id,
 name,
) VALUES ();
INSERT INTO image_soundtrack_type (
 id,
 name,
) VALUES ();
INSERT INTO language (
 id,
 name,
 code ,
) VALUES ();
INSERT INTO stage_developer_type (
 id,
 name,
) VALUES ();
INSERT INTO source (
 id,
 name,
 url_base ,
) VALUES ();
INSERT INTO collaborator_type (
 id,
 name,
) VALUES ();
INSERT INTO collection (
 id,
 name,
 description TEXT,
) VALUES ();
INSERT INTO compose_type (
 id,
 name,
) VALUES ();
INSERT INTO condition_type (
 id,
 name,
) VALUES ();
INSERT INTO company_function_type (
 id,
 name,
) VALUES ();
INSERT INTO soundtrack_type (
 id,
 name,
) VALUES ();
INSERT INTO blood_type (
 id,
 name,
) VALUES ();
INSERT INTO box_condition_type (
 id,
 name,
) VALUES ();
INSERT INTO audio_codec (
 id,
 name,
) VALUES ();
INSERT INTO based_type (
 id,
 name,
) VALUES ();
INSERT INTO collaborator (
 id,
 name,
 irc ,
 description TEXT,
 create_date
) VALUES ();
INSERT INTO tag (
 id,
 name,
) VALUES ();
INSERT INTO category (
 id,
 name,
) VALUES ();
INSERT INTO classification_type (
 id,
 name,
) VALUES ();
INSERT INTO edition_type (
 id,
 name,
) VALUES ();
INSERT INTO currency (
 id,
 name,
 symbol ,
 code ,
) VALUES ();
INSERT INTO country (
 id,
 name,
 code ,
) VALUES ();
INSERT INTO software_type (
 id,
 name,
) VALUES ();
INSERT INTO social (
 id,
 social_type_id,
 url,
) VALUES ();
INSERT INTO lists_figure (
 id,
 user_id,
 name,
 create_date
) VALUES ();
INSERT INTO urls (
 source_id,
 link,
 last_checked
) VALUES ();
INSERT INTO version (
 id,
 stage_developer_type_id,
 number,
 changelog TEXT
) VALUES ();
INSERT INTO collaborator_website (
 collaborator_id,
 website,
) VALUES ();
INSERT INTO event (
 id,
 currency_id,
 name,
 location,
 website,
,
 duration,
) VALUES ();
INSERT INTO company (
 id,
 country_id,
 name,
 social_name,
 start_year CHAR(4),
 website,
 description TEXT,
 create_date,
) VALUES ();
INSERT INTO user_email (
 user_id,
 email,
) VALUES ();
INSERT INTO soundtrack (
 id,
 soundtrack_type_id,
 name,
 launch_year CHAR(4),
) VALUES ();
INSERT INTO requirements (
 id,
 version_id,
 video_board,
 processor,
 memory,
 hd_storage,
) VALUES ();
INSERT INTO driver (
 id,
 requirements_id,
 name,
) VALUES ();
INSERT INTO people (
 id,
 country_id,
 blood_type_id,
 name,
 last_name,
 website,
 description TEXT,
) VALUES ();
INSERT INTO people_nacionalization (
 people_id,
 country_id,
) VALUES ();
INSERT INTO collaborator_has_social (
 social_id,
 collaborator_id,
 create_date,
 last_checked,
) VALUES ();
INSERT INTO shops_operate_on_country (
 shops_id,
 country_id,
) VALUES ();
INSERT INTO company_has_social (
 social_id,
 company_id,
 last_checked,
 create_date,
) VALUES ();
INSERT INTO people_has_social (
 social_id,
 people_id,
 last_checked,
 create_date,
) VALUES ();
INSERT INTO collaborator_has_member (
 collaborator_id,
 member_id,
 founder,
) VALUES ();
INSERT INTO soundtrack_integrate_collection (
 collection_id,
 soundtrack_id,
) VALUES ();
INSERT INTO audio (
 id,
 country_id,
 audio_codec_id,
 name,
 duration,
 bitrate,
) VALUES ();
INSERT INTO audio_has_language (
 audio_id,
 language_id,
) VALUES ();
INSERT INTO company_has_country (
 country_id,
 company_id,
) VALUES ();
INSERT INTO country_has_currency (
 currency_id,
 country_id,
 main,
) VALUES ();
CREATE TABLE tag_has_filter_type (
  user_filter_type_id,
  tag_id,
) VALUES ();
INSERT INTO company_sponsors_event (
 company_id,
 event_id,
) VALUES ();
INSERT INTO company_owner_collection (
 company_id,
 collection_id,
) VALUES ();
INSERT INTO user_filter (
 id,
 filter_type_id,
 user_id,
 dont_show_content,
) VALUES ();
CREATE TABLE category_has_filter_type (
  category_id,
  filter_type_id,
) VALUES ();
INSERT INTO lists_edition (
 id,
 entity_type_id,
 user_id,
 name,
 create_date,
) VALUES ();
INSERT INTO lists_release (
 id,
 entity_type_id,
 user_id,
 name,
 create_date,
) VALUES ();
INSERT INTO users_has_social (
 user_id,
 social_id,
 last_checked,
 create_date,
) VALUES ();
INSERT INTO country_has_language (
 language_id,
 country_id,
) VALUES ();
INSERT INTO genre_type_has_audio (
 genre_type_id,
 audio_id,
) VALUES ();
INSERT INTO people_has_image (
 image_id,
 people_id,
) VALUES ();
INSERT INTO soundtrack_has_image (
 soundtrack_id,
 image_id,
 image_soundtrack_type_id,
) VALUES ();
INSERT INTO people_compose_audio (
 audio_id,
 people_id,
 compose_type_id,
) VALUES ();
INSERT INTO lyrics (
 id,
 lyric_type_id,
 user_id,
 audio_id,
 language_id,
 lyric TEXT,
) VALUES ();
INSERT INTO entity (
 id,
 entity_type_id,
 classification_type_id,
 collection_id,
 language_id,
 country_id,
 title,
 romanized_title,
 subtitle,
 synopse TEXT,
 launch_year CHAR(4),
 collection_started,
) VALUES ();
INSERT INTO archive (
 id,
 version_id,
 name,
 url,
 size,
 extension,
) VALUES ();
INSERT INTO alias (
 id,
 people_id,
 name,
) VALUES ();
INSERT INTO entity_associated_name (
 id,
 entity_id,
 name,
) VALUES ();
INSERT INTO persona (
 id,
 blood_type_id,
 entity_id,
 name,
 personage_gender gender,
 first_appear_on,
 height,
 weight ,
 eyes_color,
 hair_color,
) VALUES ();
INSERT INTO soundtrack_has_audio (
 soundtrack_id,
 audio_id,
 exclusive,
) VALUES ();
INSERT INTO entity_has_tag (
 tag_id,
 entity_id,
) VALUES ();
INSERT INTO entity_has_category (
 entity_id,
 category_id,
) VALUES ();
INSERT INTO hash (
 id,
 hash_type_id,
 archive_id,
 code TEXT,
 create_date,
) VALUES ();
INSERT INTO people_produces_entity (
 people_id,
 entity_id,
 production_type_id,
) VALUES ();
INSERT INTO entity_has_entity (
 entity_id,
 other_entity_id,
 based_type_id,
) VALUES ();
INSERT INTO persona_related_persona (
 persona_id,
 other_persona_id,
 related_type_id,
) VALUES ();
INSERT INTO entity_edition (
 id,
 edition_type_id,
 event_id,
 entity_id,
 title,
 free,
 release_description TEXT,
 censored,
 code,
 complement_code,
 height,
 width,
 depth,
 weight ,
) VALUES ();
INSERT INTO software_edition (
 entity_edition_id,
 plataform_type_id,
 software_type_id,
 media_type_id,
) VALUES ();
INSERT INTO entity_release (
 id,
 entity_id,
 release_type_id,
 country_id,
 entity_edition_id,
 description TEXT,
 release_date,
) VALUES ();
INSERT INTO lists_release_list_entity_release (
 lists_release_id,
 entity_release_id,
 release_read_status_type_id,
 release_ownership_type_id,
 local_storage,
) VALUES ();
INSERT INTO figure (
 id,
 entity_id,
 figure_version_id,
 currency_id,
 scale_id,
 country_id,
 height ,
 width ,
 weight ,
 launch_price ,
 release_date,
 observation TEXT,
) VALUES ();
INSERT INTO lists_figure_list_figure (
 lists_figure_id,
 figure_id,
 ownership_status_id,
 box_condition_type_id,
 product_condition_type_id,
 observation TEXT,
) VALUES ();
INSERT INTO lists_edition_list_entity_edition (
 lists_edition_id,
 entity_edition_id,
 ownership_status_id,
 condition_type_id,
 read_status_type_id,
) VALUES ();
INSERT INTO persona_race (
 id,
 persona_id,
 name,
) VALUES ();
INSERT INTO persona_occupation (
 id,
 persona_id,
 occupation,
) VALUES ();
INSERT INTO persona_unusual_features (
 id,
 persona_id,
 name,
) VALUES ();
INSERT INTO persona_affiliation (
 id,
 persona_id,
 name,
) VALUES ();
INSERT INTO persona_associated_name (
 id,
 persona_id,
 name,
) VALUES ();
INSERT INTO game_release (
 entity_release_id,
 emulate,
 installation_instructions TEXT,
) VALUES ();
INSERT INTO soundtrack_for_entity_edition (
 soundtrack_id,
 entity_edition_id,
) VALUES ();
INSERT INTO software_subtitle (
 software_edition_entity_edition_id,
 language_id,
) VALUES ();
INSERT INTO read_edition (
 entity_edition_id,
 print_type_id,
 pages_number,
 chapters_number,
) VALUES ();
INSERT INTO figure_has_tag (
 tag_id,
 figure_id,
) VALUES ();
CREATE TABLE entity_edition_subtitle (
  language_id,
  entity_edition_id,
) VALUES ();
INSERT INTO software_edition_has_version (
 software_edition_entity_edition_id,
 version_id,
) VALUES ();
INSERT INTO entity_release_has_language (
 entity_release_id,
 language_id,
) VALUES ();
INSERT INTO entity_edition_launch_country (
 entity_edition_id,
 country_id,
 launch_date,
 launch_price ,
) VALUES ();
INSERT INTO entity_edition_has_currency (
 entity_edition_id,
 currency_id,
) VALUES ();
INSERT INTO entity_edition_has_language (
 entity_edition_id,
 language_id,
) VALUES ();
INSERT INTO figure_has_shops (
 figure_id,
 shops_id,
 product_url,
 checked_last,
) VALUES ();
INSERT INTO figure_has_shop_location (
 figure_id,
 shop_location_id,
) VALUES ();
INSERT INTO figure_has_material (
 figure_id,
 material_id,
) VALUES ();
INSERT INTO entity_release_has_version (
 entity_release_id,
 version_id,
) VALUES ();
INSERT INTO figure_from_persona (
 figure_id,
 persona_id,
) VALUES ();
INSERT INTO category_has_figure (
 category_id,
 figure_id,
) VALUES ();
INSERT INTO comments (
 id,
 entity_release_id,
 user_id,
 content TEXT,
 title,
 create_date,
) VALUES ();
INSERT INTO mod (
 id,
 entity_release_id,
 mod_type_id,
 name,
 author,
 launch_date,
 version,
 description TEXT,
 installation_instruction TEXT,
) VALUES ();
INSERT INTO mod_has_image (
 mod_id,
 image_id,
) VALUES ();
INSERT INTO company_produces_figure (
 company_id,
 figure_id,
 produces_figure_type_id,
) VALUES ();
INSERT INTO member_produces_entity_release (
 member_id,
 entity_release_id,
 function_type_id,
) VALUES ();
INSERT INTO collaborator_provides_release (
 collaborator_id,
 entity_release_id,
 collaborator_type_id,
) VALUES ();
INSERT INTO people_produces_figure (
 people_id,
 figure_id,
 produces_type_id,
) VALUES ();
INSERT INTO company_has_entity_edition (
 company_id,
 entity_edition_id,
 company_function_type_id,
) VALUES ();
INSERT INTO number_release (
 id,
 entity_release_id,
 number_type_id,
 entity_type_id,
 number,
) VALUES ();
INSERT INTO entity_edition_has_image (
 image_id,
 entity_edition_id,
 image_edition_type_id,
) VALUES ();
INSERT INTO figure_has_image (
 image_id,
 figure_id,
 image_figure_type_id
) VALUES ();
INSERT INTO number_edition (
 id,
 entity_edition_id,
 number_type_id,
 entity_type_id,
 number
) VALUES ();