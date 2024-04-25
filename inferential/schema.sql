create table requests if not exists(
  model text,
  time integer default (strftime('%s','now')),
  input_tokens text,
  output_tokens text
);

create index idx_log_table_model 
on requests(model);