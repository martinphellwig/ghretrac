"""
Identity, Name, Address, Contact and Relation

We use an internal UUID table to uniquely identify a person.
Since addresses and contact data could possibly shared, there is an explicit
m2m type table between the UUID and for example the Address table called
UAddress.
"""
from django.db import models
from django.db.models.signals import post_init
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone

import uuid
import hashlib

# pylint: disable=too-few-public-methods, no-member, unused-argument

class _CustomManager(models.Manager):
    """This hooks into the _Abstract Model and will prevent prevent models to be
    loaded that have been marked as deleted.
    """
    def __init__(self, *args, **kwargs):
        super(_CustomManager, self).__init__(*args, **kwargs)

    def all(self):
        "Return all except that have been deleted."
        return super(_CustomManager, self).all().\
                                                filter(dts_delete__isnull=True)

    def filter(self, *args, **kwargs):
        "As normal filter but exclude deleted objects."
        return super(_CustomManager, self).filter(*args, **kwargs)\
                                               .filter(dts_delete__isnull=True)

    def filter_include_delete(self, *args, **kwargs):
        "Behaves as the original filter."
        return super(_CustomManager, self).filter(*args, **kwargs)


class _Abstract(models.Model):
    """
    All models should inherit from here, this adds convenient timestamps.
    """
    objects = _CustomManager()

    class Meta:
        """
        Make sure that django knows this is a meta field.
        """
        abstract = True

    dts_insert = models.DateTimeField(auto_now_add=True)
    dts_update = models.DateTimeField(auto_now=True)
    dts_delete = models.DateTimeField(null=True, blank=True, editable=False)

    def delete(self, using=None):
        self.dts_delete = timezone.now()
        self.save()

    def is_active(self):
        "If this record is active return True otherwise False"
        if self.dts_delete == None:
            return True

        return False

    def _str_prefix(self, value):
        "Prefix for a record, indicating active/inactive"
        if self.is_active():
            prefix = '[_] '
        else:
            prefix = '[X] '

        return prefix + value


# NameSpace base OID = 1.3.6.1.4.1.44797
# This is the OID of stoatworks.
# 1.3.6.1.4.1.44797.1 # the UUID category
# 1.3.6.1.4.1.44797.1.1 # sub category derived from a hashed value
# In our case we use the settings.SECRET_KEY, so the base OID is going to be:
_OID = hashlib.sha224(settings.SECRET_KEY.encode('UTF-8')).digest()
_OID = str(int.from_bytes(_OID, byteorder='big', signed=False))
_OID = '1.3.6.1.4.1.44797.1.1.' + _OID

class UUID(_Abstract):
    """
    Universal Unique Identifier
    The base reference to uniquely identify a person or organisation, most other
    tables will refer to this one.
    The same company or person may be known by multiples names, but it will have
    the same uuid. When we make a reference, we reference to the uuid field.
    This means that when we later need to merge two databases we can do that
    with this process:
    1 - For each uuid that exists in both databases and that are indeed not the
        same, create a new uuid and update references.
    2 - For each collection of uuid that should be the same, use the oldest
        uuid and update references.
    3 - Import data into the database.
    4 - For each uuid see if there is duplicate data and merge where possible.
    """
    uuid = models.CharField(unique=True, max_length=36, null=True,
                            editable=False,
                            help_text="UUID RFC4122 compliant (uuid5)")
    poid = models.CharField(default=_OID, max_length=90, editable=False,
                            help_text="The parents OID")

    def __str__(self):
        return self._str_prefix(str(getattr(self, 'uuid')))

    class Meta:
        "Meta"
        verbose_name = "UUID"
        verbose_name_plural = "UUIDs"


@receiver(post_init, sender=UUID)
def _set_uuid(sender, **kwargs):
    "Hook into the post init so we always have a uuid generated."
    if 'instance' not in kwargs:
        return

    instance = kwargs['instance']
    if instance.id != None and instance.uuid == None:
        value = instance.poid + '.' + str(instance.id)
        instance.uuid = str(uuid.uuid5(uuid.NAMESPACE_OID, value))
        instance.save()


# Identifiers
class IdentityType(_Abstract):
    """
    What type of identity this is, e.g. UK NIN, paypal ID, etc.
    """
    value = models.CharField(unique=True, max_length=128)
    regex = models.TextField(null=True, blank=True)

    class Meta:
        "Meta"
        verbose_name = "IdentityType"
        verbose_name_plural = "IdentityTypes"

    def __str__(self):
        return self._str_prefix(self.value)


class UIdentities(_Abstract):
    """
    External identity associated with an UUID.
    """
    uuid = models.ForeignKey(UUID, 'uuid')
    value = models.CharField(unique=True, max_length=128)
    value_type = models.ForeignKey(IdentityType)

    def __str__(self):
        tmp = [self.uuid.uuid, str(self.value_type), self.value]
        return self._str_prefix(' - '.join(tmp))

    class Meta:
        "Meta"
        verbose_name = "UIdentity"
        verbose_name_plural = "UIdentities"


# Name Table
class UName(_Abstract):
    """
    The name of the person.
    """
    uuid = models.ForeignKey(UUID, 'uuid')
    first = models.CharField(max_length=32,
                             help_text="Given name of person")
    # Go by is distinctive from first, for example a first name may be Alexander
    # but the customer may want to be called Lex in non-offical communication.
    go_by = models.CharField(max_length=32, null=True, blank=True,
                             help_text="The name the person goes by")
    middle = models.TextField(null=True, blank=True,
                              help_text="All middle names")
    # Such as 'de la', 'van den' and 'von'
    prefix = models.CharField(max_length=16, null=True, blank=True,
                             help_text="Prefix to the family name")
    family = models.TextField(help_text="The surname")
    # Such as a number or Junior/Senior
    affix = models.CharField(max_length=16, null=True, blank=True,
                             help_text="Affix to the family name")
    official = models.TextField(
                               help_text="The official names, including titles")

    def __str__(self):
        return self._str_prefix(str(self.official) + \
                                ' {' + self.uuid.uuid + '}')

    class Meta:
        "Meta"
        verbose_name = "uName"
        verbose_name_plural = "uNames"


# Address related tables
class Address(_Abstract):
    """
    The value type where the other table must choose from.
    """
    name = models.CharField(max_length=128, null=True, blank=True,
                            help_text='If name is given use that over UName.')
    line_1 = models.CharField(max_length=40)
    line_2 = models.CharField(max_length=40, null=True, blank=True)
    line_3 = models.CharField(max_length=40, null=True, blank=True)
    line_4 = models.CharField(max_length=40, null=True, blank=True)
    line_5 = models.CharField(max_length=40, null=True, blank=True)
    code = models.CharField(max_length=16, null=True, blank=True)
    city = models.CharField(max_length=64)
    region = models.CharField(max_length=64, null=True, blank=True)
    country = models.CharField(max_length=2)

    def __str__(self):
        address = [self.line_1, self.line_2, self.line_3, self.line_4,
                   self.line_5, self.code, self.city, self.region, self.country]
        text = '\n'.join([item for item in address if item !=None])
        return self._str_prefix(text)

    class Meta:
        "Meta"
        verbose_name = "Address"
        verbose_name_plural = "Addresses"


class UAddress(_Abstract):
    """
    The address tied to the UUID.
    """
    uuid = models.ForeignKey(UUID, 'uuid')
    address = models.ForeignKey(Address)

    class Meta:
        "Meta"
        verbose_name = "uAddress"
        verbose_name_plural = "uAddresses"

    def __str__(self):
        return self._str_prefix(self.uuid.uuid + ' - ' + str(self.address))


# Contact Related Tables
class ContactType(_Abstract):
    """
    What type of contact it is, .e.g. email, fax, telephone, etc.
    The regex is there so optional the value of contact (not ContactType)
    can be validated.
    """
    value = models.CharField(unique=True, max_length=128)
    regex = models.TextField(null=True, blank=True)

    class Meta:
        "Meta"
        verbose_name = "ContactType"
        verbose_name_plural = "ContactTypes"

    def __str__(self):
        return self._str_prefix(self.value)


class Contact(_Abstract):
    """
    The value type where the other table must choose from.
    """
    value = models.CharField(unique=True, max_length=128)
    value_type = models.ForeignKey(ContactType)

    class Meta:
        "Meta"
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return self._str_prefix(self.value + ' {' + self.value_type.value + '}')


class ContactCategory(_Abstract):
    """
    What category is the contact, e.g. home, office, out-of-hours, etc.
    """
    value = models.CharField(unique=True, max_length=128)

    class Meta:
        "Meta"
        verbose_name = "ContactCategory"
        verbose_name_plural = "ContactCategories"

    def __str__(self):
        return self._str_prefix(self.value)


class UContact(_Abstract):
    """
    Name values
    """
    uuid = models.ForeignKey(UUID, 'uuid')
    contact = models.ForeignKey(Contact)
    category = models.ForeignKey(ContactCategory)

    class Meta:
        "Meta"
        verbose_name = "uContact"
        verbose_name_plural = "uContacts"

    def __str__(self):
        tmp = [self.uuid.uuid, str(self.contact), str(self.category)]
        return self._str_prefix(' - '.join(tmp))


# Relation Tables
class RelationType(_Abstract):
    """
    What is the relation between one and two, e.g. father/mother/guardian.
    """
    value = models.CharField(unique=True, max_length=128)

    class Meta:
        "Meta"
        verbose_name = "RelationType"
        verbose_name_plural = "RelationTypes"

    def __str__(self):
        return self._str_prefix(self.value)


class URelation(_Abstract):
    """
    Define relation between two UUIDs.
    """
    uuid_one = models.ForeignKey(UUID, 'uuid', related_name='uuid_one')
    uuid_two = models.ForeignKey(UUID, 'uuid', related_name='uuid_two')
    relation = models.ForeignKey(RelationType)

    class Meta:
        "Meta"
        verbose_name = "uRelation"
        verbose_name_plural = "uRelations"

    def __str__(self):
        tmp = [self.uuid_one.uuid, self.uuid_two.uuid, self.relation.value]
        return self._str_prefix(' - '.join(tmp))


def get_name(uuid_object):
    "Get the name via uuid"
    query = uuid_object.uname_set.all().order_by('dts_update').reverse()
    if query.exists():
        return query[0]
    else:
        return None

def get_email(uuid_object):
    "Get the email via uuid"
    query = uuid_object.ucontact_set.filter(contact__value_type__value='email')\
                                               .order_by('dts_update').reverse()
    if query.exists():
        return query[0].contact.value
    else:
        return None

def get_phone(uuid_object):
    "Get the phone via uuid"
    query = uuid_object.ucontact_set.filter(
        contact__value_type__value='telephone').order_by('dts_update').reverse()

    if query.exists():
        return query[0].contact.value
    else:
        return None

def get_address(uuid_object):
    "Get the address via uuid"
    query = uuid_object.uaddress_set.all().order_by('dts_update').reverse()

    if query.exists():
        return query[0].address
    else:
        return None

