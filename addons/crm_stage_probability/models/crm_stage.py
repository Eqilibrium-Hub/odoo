# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import fields, models


class CrmStage(models.Model):

    _inherit = "crm.stage"

    probability = fields.Float(
        "Probability (%)",
        required=True,
        default=10.0,
        help="This percentage depicts the default/average probability of the "
        "Case for this stage to be a success",
    )

    _sql_constraints = [
        (
            "check_probability",
            "check(probability >= 0 and probability <= 100)",
            "The probability should be between 0% and 100%!",
        )
    ]
