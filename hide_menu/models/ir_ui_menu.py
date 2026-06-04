# -*- coding: utf-8 -*-
from odoo import models,fields

class IrUiMenu(models.Model):


    _inherit = 'ir.ui.menu'

    def _filter_visible_menus(self):
        """ Filter `self` to only keep the menu items that should be visible in
            the menu hierarchy of the current user.
            Uses a cache for speeding up the computation.
        """
        menu=super()._filter_visible_menus()
        hidden_menu=self.env.user.hide_specific_menu
        print(hidden_menu)
        res=menu-hidden_menu
        print(res)
        return res



