{
	'name': 'Account Simplified Journal',
	'version': '0.1',
	'category': 'Accounting',
	'description': """
		Simplify journal entries by storing preset transactions in a master and let user 
		choose them for default journal, accounts, and autoposting.
	""",
	'author': 'Christyan Juniady and Associates',
	'maintainer': 'Christyan Juniady and Associates',
	'website': 'http://www.chjs.biz',
	'depends': ["base","account"],
	'sequence': 150,
	'data': [
		'views/account_simplified_journal_view.xml',
	],
	'demo': [
	],
	'test': [
	],
	'update_xml': [
	],
	'installable': True,
	'auto_install': False,
	'qweb': [
	]
}
