from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    def _get_default_chatgpt_model(self):
        return self.env.ref('chatgpt_base.chatgpt_model_gpt_4_1106_preview').id

    openapi_api_key = fields.Char(string="API Key", help="Provide the API key here", config_parameter="chatgpt_base.openapi_api_key")
    chatgpt_model_id = fields.Many2one('chatgpt.model', 'ChatGPT Model', ondelete='cascade',
                                       default=_get_default_chatgpt_model,  config_parameter="chatgpt_base.chatgpt_model")
