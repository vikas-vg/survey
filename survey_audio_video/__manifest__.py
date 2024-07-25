{
    "name": "Support Video in the Questions Background ( only works in One page, one question mode)",
    "summary": """
        This module add Video in Questions Background. Also able to add video video at start and end of the module""",
    "version": "16.0.1.0.0",
    "author": "Vikas Goyal",
    "email": "info.vikasgoyal@gmail.com",
    "company": "",
    "website": "",
    "depends": ["survey", "web_widget_video"],
    "data": [
        "views/survey_question_view.xml",
        "views/survey_survey_view.xml",
        "views/templates.xml",
    ],
    "assets": {
        "survey.survey_assets": [
            "survey_audio_video/static/src/scss/survey_background_video.scss",
            # "survey_audio_video/static/src/js/survey.js",
        ]
    },
    "application": True
}
