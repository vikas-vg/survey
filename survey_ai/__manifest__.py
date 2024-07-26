{
    "name": "Generate AI Questions",
    "summary": "Generate Questions Using AI (chatGPT)",
    "version": "16.0.1",
    "license": "LGPL-3",
    "author": "Vikas Goyal",
    "email": "info.vikasgoyal@gmail.com",
    "company": "",
    "website": "",
    "category": "survey",
    "depends": ["survey", "chatgpt_base"],
    "data": [
        "security/ir.model.access.csv",
        "views/survey_generate_question_view.xml",
        "views/survey_survey_view.xml",
    ],
    "application": True,
    "installable": True,
}
