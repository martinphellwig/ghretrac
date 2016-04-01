"""
Setup original data
"""

DATA = [{('inacar', 'IdentityType'):[{'header':['value'],
                                      'values':[['paypal'],],
                                      }],
         },
        {('inacar', 'ContactCategory'):[{'header':['value'],
                                         'values':[['home'],
                                                   ['office'],
                                                   ['mobile'],],
                                      }],
         },
        {('inacar', 'ContactType'):[{'header':['value'],
                                     'values':[['email'],
                                               ['telephone'],
                                               ['fax'],
                                               ['twitter'],
                                               ['g+'],
                                               ['facebook'],
                                               ['instagram'],],
                                      }],
         },
        ]


def _setup_data(apps):
    "Walk through DATA and add the values."
    #pylint: disable=star-args, invalid-name
    for data_import in DATA:
        for model_app, data in data_import.items():
            _Class = apps.get_model(*model_app)
            tmp = list()
            for instance in data:
                attributes = instance['header']
                for values in instance['values']:
                    inits = dict(zip(attributes, values))
                    tmp.append(_Class(**inits))
            _Class.objects.bulk_create(tmp)

def setup_data(apps, schema_editor):
    #pylint: disable=unused-argument
    "Execute setup"
    _setup_data(apps)
