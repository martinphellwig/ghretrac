'''
Created on 13 Mar 2015

@author: martin
'''
from django.dispatch import receiver, Signal

from paypal.signals import paypal_ipn
from . import models

#pylint: disable=invalid-name
inacar_add = Signal(providing_args=["uuid", "ipn"])

# pylint: disable=no-member, star-args
def _name(uuid, instance):
    "Add name if it doesn't exists"
    if models.UName.objects.filter(uuid=uuid).exists():
        name =  models.UName.objects.filter(uuid=uuid)[0]
    else:
        maps = [('first', 'first_name'),
                ('go_by', 'first_name'),
                ('family', 'last_name')]

        kwargs = dict()
        for key_args, key_from in maps:
            kwargs[key_args] = instance.data.get(key_from, '')

        kwargs['uuid'] = uuid
        kwargs['official'] = kwargs['first'] + ' ' +  kwargs['family']

        name = models.UName.objects.create(**kwargs)

    return name

def _address(uuid, instance):
    "Add address if it doesn't exists."
    if models.UAddress.objects.filter(uuid=uuid).exists():
        pass
    else:
        maps = [('name', 'address_name'),
                ('line_1','address_street'),
                ('code','address_zip'),
                ('city','address_city'),
                ('region', 'address_state'),
                ('country','address_country_code'),
                ]
        kwargs = dict()
        for key_args, key_from in maps:
            if key_from in instance.data:
                kwargs[key_args] = instance.data[key_from]

        if 'name' in kwargs:
            name = _name(uuid, instance)
            if kwargs['name'].strip().lower() == name.official.strip().lower():
                kwargs.pop('name')

        if 'payer_business_name' in instance.data:
            kwargs['line_2'] = kwargs['line_1']
            kwargs['line_1'] = instance.data['payer_business_name']

        address = models.Address.objects.get_or_create(**kwargs)[0]
        uaddress = models.UAddress()
        uaddress.uuid = uuid
        uaddress.address = address
        uaddress.save()


def _uuid(instance):
    "Add UUID if it can't be found."
    paypal = models.IdentityType.objects.get(value='paypal')
    kwargs = {'value':instance.data['payer_id'], 'value_type':paypal}
    qst = models.UIdentities.objects.filter(**kwargs)
    if qst.exists():
        uuid = qst[0].uuid
    else:
        uuid = models.UUID.objects.create()
        uuid = models.UUID.objects.get(id=uuid.id)

        kwargs['uuid'] = uuid
        models.UIdentities.objects.create(**kwargs)

    return uuid

def _contact(instance, contact_type, key_paypal):
    "Add or retrieve contact"
    kwargs = {'value_type':contact_type,
              'value':instance.data[key_paypal].strip().lower()}
    query = models.Contact.objects.filter_include_delete(**kwargs)
    if query.exists():
        for item in query:
            item.dts_delete = None
            item.save()
    else:
        query = models.Contact.objects.get_or_create(**kwargs)

    return query[0]


def _home_contact(uuid, instance, key_paypal, key_inacar):
    "Add home contact"
    if instance.data.get(key_paypal, '').strip() != '':
        contact_type = models.ContactType.objects.get(value=key_inacar)
        contact = _contact(instance, contact_type, key_paypal)

        kwargs = {'uuid':uuid, 'contact':contact}
        qst = models.UContact.objects.filter(**kwargs)
        if not qst.exists():
            kwargs['category'] = models.ContactCategory.objects.get(
                                                                   value='home')
            models.UContact.objects.create(**kwargs)

def _email(uuid, instance):
    "Add email"
    _home_contact(uuid, instance, 'payer_email', 'email')

def _phone(uuid, instance):
    "Add phone"
    _home_contact(uuid, instance, 'contact_phone', 'telephone')

@receiver(paypal_ipn)
def handler_paypal_ipn(sender, instance, **kwargs):
    #pylint: disable=unused-argument
    """
    Handle a paypal IPN
    For INACAR purposes we are not interested what kind of message it is, we
    handle all of them to fill the the tables with the relevant data.
    """
    if not 'payer_id' in instance.data:
        return

    uuid = _uuid(instance)
    _address(uuid, instance)
    _email(uuid, instance)
    _phone(uuid, instance)
    inacar_add.send(sender=handler_paypal_ipn, uuid=uuid, ipn=instance)



