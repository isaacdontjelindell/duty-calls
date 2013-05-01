db.define_table('locations',
    Field('location_name','string', unique=True),
    Field('calendar_url','string'),
    Field('twilio_number_id','string'),
    Field('is_res_life','boolean'),
    Field('contact_dict', 'json')
)
