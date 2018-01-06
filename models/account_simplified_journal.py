from openerp import SUPERUSER_ID
from openerp.osv import osv, fields
from openerp.tools.translate import _
from datetime import datetime, date, timedelta

class account_journal_preset(osv.osv):

	_name = 'account.journal.preset'
	_description = 'Master preset journal'

	_columns = {
		'name': fields.char('Name', size=125, required=True),
		'code': fields.char('Code', help="A unique identifier to be referenced in program code."),
		'journal_id': fields.many2one('account.journal', 'Journal', required=True),
		'default_debet_account_id': fields.many2one('account.account', 'Default debet account', required=True),
		'default_credit_account_id': fields.many2one('account.account', 'Default credit account', required=True),
		'auto_post': fields.boolean('Autoposting?'),
	}

	_defaults = {
		'auto_post': False,
	}

	_sql_constraints = [
		('unique_name','UNIQUE(name)',_('Name must be unique.')),
		('unique_code','UNIQUE(code)',_('Code must be unique.')),
		('debet_credit_no_equal','CHECK(default_debet_account_id <> default_credit_account_id)',_('Debet and Credit account must not be the same.')),
	]

class account_journal_simplified(osv.osv):

	_name = 'account.journal.simplified'
	_description = 'Simplified journal entries'

	_columns = {
		'name': fields.char('Description'),
		'journal_date': fields.datetime('Transaction Date', required=True),
		'preset_id': fields.many2one('account.journal.preset', 'Transaction Type', required=True),
		'amount': fields.float('Amount', required=True),
	}

	_defaults = {
		'journal_date': lambda self, cr, uid, context: datetime.now(),
	}

	def _get_debet_account(self, cr, uid, transaction_id, preset, context={}):
	# overridable by inheriting modules
		return preset.default_debet_account_id.id

	def _get_credit_account(self, cr, uid, transaction_id, preset, context={}):
	# overridable by inheriting modules
		return preset.default_credit_account_id.id

	def create(self, cr, uid, vals, context={}):
		new_id = super(account_journal_simplified, self).create(cr, uid, vals, context)
		preset = self.pool.get('account.journal.preset').browse(cr, uid, vals['preset_id'])
		journal_entry_obj = self.pool.get('account.move')
		name = vals.get('name') or preset.name
		entry_data = journal_entry_obj.account_move_prepare(cr, uid, preset.journal_id.id, date=vals.get('journal_date'), ref=name)
		entry_data['line_id'] = [
			[0,False,{
				'name': name, 
				'account_id': self._get_debet_account(cr, uid, new_id, preset, context), 
				'debit': vals.get('amount', 0),
				'credit': 0,
			}],
			[0,False,{
				'name': name, 
				'account_id': self._get_credit_account(cr, uid, new_id, preset, context), 
				'credit': vals.get('amount', 0),
				'debit': 0,
			}],
		]
		new_entry_id = journal_entry_obj.create(cr, uid, entry_data, context=context)
		if preset.auto_post:
			journal_entry_obj.post(cr, uid, [new_entry_id], context=context)
		return new_id