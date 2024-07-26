{
    'name': 'Odoo ChatGPT Integration',
    'version': '16.0.1.1.0',
    'license': 'AGPL-3',
    'summary': 'Odoo ChatGPT Integration',
    'description': 'Allows the application to leverage the capabilities of the GPT language model to generate human-like responses, providing a more natural and intuitive user experience',
    'author': 'Vikas Goyal',
    'company': "",
    'depends': ['base', 'base_setup'],
    'data': [
        'security/ir.model.access.csv',
        'data/chatgpt_model_data.xml',
        'views/res_config_settings_views.xml',
    ],
    'external_dependencies': {'python': ['openai']},
    'installable': True,
    'application': False,
    'auto_install': False,
}
