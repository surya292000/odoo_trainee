# -*- coding: utf-8 -*-
"""
Main Model of Example Application
"""
from odoo import fields,models

class Example(models.Model):

    _name = 'example'
    _description = 'Example'

    name = fields.Char('Name',required=True)
    partner_id = fields.Many2one('res.partner','Customer')
    example_line_ids = fields.One2many('example.line',
                                       'example_id',
                                       string='Example Lines')
    example_tag_ids = fields.Many2many('example.tag',string='Tags')

    def action_test(self):
        product=self.env['product.product'].search([],order='id desc',limit=1)
        print('product',product,product.name)
        # self.example_line_ids=[fields.Command.create({
        #     'product_id':product.id,
        #     'qty':1,
        #     'price':10
        # })]
        # print(self.read(),self.env["product.product"])
        # self.example_line_ids.create({
        #     'product_id': product.id,
        #     'qty': 1,
        #     'price': 10,
        #     'example_id':self.id
        # })
        # print("sdfghj")

        # line=self.example_line_ids.search([('price','=',0)])
        # print(line)
        # for record in self.example_line_ids:
        #     if record.qty == 15:
        #         self.example_line_ids=[fields.Command.update(record.id,{
        #             'qty': 1
        #     })]
        #
        # self.example_line_ids = [fields.Command.update(record.id,{'qty' : 1}) for record in self.example_line_ids if record.qty ==15 ]
        #
        # for record in self.example_line_ids.filtered(lambda line: line.qty == 15):
        #     self.example_line_ids=[fields.Command.update(record.id,{
        #             'qty': 1
        #     })]

        # for record in self.example_line_ids:
        #     if record.price == 0:
        #         record.price = 15
        #
        # self.example_line_ids.filtered(lambda line: line.price == 15).unlink({
        #     'price' : 0
        # })

        # self.example_line_ids = [fields.Command.unlink(rec.id) for rec in self.example_line_ids if rec.price==0]
        # self.example_line_ids = [fields.Command.delete(rec.id) for rec in self.example_line_ids]

        # unlinked_ids = self.example_line_ids.search([('example_id','=',False)])
        # self.example_line_ids = [fields.Command.unlink(rec.id) for rec in unlinked_ids]
        # print(unlinked_ids)

        # self.unlink()_record
        # linked_ids = self.example_line_ids.filtered(lambda  line: line.price == 0)
        # print(linked_ids)
        #
        # linked_ids_orm = self.example_line_ids.search([('price','=',0),('example_id','=',self.id)]).write({
        #     'example_id':False
        # })
        # print(linked_ids_orm)

        # self.example_line_ids = [fields.Command.set(unlinked_ids.ids)]
        # rec = self.env.ref("example.tag_new")
        # self.example_tag_ids = [fields.Command.link(rec.id)]
        rec = self.example_line_ids.filtered(lambda i: i.qty > 10).sorted('price',reverse=True).mapped('price')
        print(self.example_line_ids.example_id)
        # total = sum(self.example_line_ids.filtered(lambda i: i.qty > 10).mapped('sub_total'))

        print(rec)
        # self.example_line_ids = [fields.Command.clear()]+unlinked_list
















