create table form1 (
    id integer primary key,
    template_name text not null,
    background_colour text not null,
    background_image text not null,
    height text not null,
    content_bg_clr text not null,
    border_radius text not null,
    content_body text not null
);

create table form2 (
    id integer primary key,
    template_name text not null,
    background_colour text not null,
    background_image text not null,
    bg_image_alt text not null,
    content text not null
);
