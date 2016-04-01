"""
IGECAS models
"""
from django.db import models
from django.core.exceptions import ValidationError
from . import coercion
# pylint: disable=locally-disabled, too-few-public-methods, no-member

class _Abstract(models.Model):
    """
    All models should inherit from here, this adds convenient timestamps.
    """
    class Meta:
        """
        Make sure that django knows this is a meta field.
        """
        abstract = True

    dts_insert = models.DateTimeField(auto_now_add=True)
    dts_update = models.DateTimeField(auto_now=True)
    dts_delete = models.DateTimeField(null=True, blank=True, editable=False)


class Person(_Abstract):
    """
    This table serves as a connector to an external table that refers to an
    individual, the reason for its existence is so that the datapoints can be
    used out of the context of the individual and thus ensuring anonymity.
    """
    identifier = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.identifier


class Origin(_Abstract):
    """
    Where does the prototype come from, e.g. Sequence, Internal, Customer
    """
    value = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.value


class Prototype(_Abstract):
    """
    What kind of prototype is this, e.g.: SNV, IDV, CUS, Derived, Survey
    """
    value = models.CharField(max_length=32, unique=True)
    origin = models.ForeignKey(Origin, related_name='prototypes')

    def __str__(self):
        return self.value +' (' + str(self.origin) + ') '


class Coercion(_Abstract):
    """
    All datapoints are stored as strings, this list functions that describe how
    a datapoint is coerced from a string to the datatype and back again.
    """
    value = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.value


class DataType(_Abstract):
    """
    DataType defines what kind of data the datapoint is, for example;
    name      = rs12913832
    description = BLUEEYE
    prototype = FK 1 (SNP)
    coercion = Enum Coercion
    """
    identifier = models.CharField(max_length=32)
    description = models.TextField(null=True, blank=True)
    prototype = models.ForeignKey(Prototype, related_name='datatypes')
    coercion = models.ForeignKey(Coercion, related_name='datatypes')

    def __str__(self):
        return self.identifier + ' (' + str(self.prototype) + ')'


class TypeValue(_Abstract):
    """
    What possible values can DataType have, this also has the confidence and
    prevalence factor defined for each value.

    value = 'GG'
    datatype = FK 1 (rs12913832)
    confidence = None (or a digit between 0.00 and 100)
    prevalence = None  (or a digit between 0.00 and 100)
    """
    value = models.CharField(max_length=64)
    datatype = models.ForeignKey(DataType, related_name='typevalues')
    confidence = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    prevalence = models.DecimalField(max_digits=5, decimal_places=2, null=True)


    def clean(self, *args, **kwargs):
        if self.confidence < 0 or self.confidence > 100:
            text = "Confidence level '%s' is not between (and including) 0-100."
            raise ValidationError(text % self.confidence)

        super(TypeValue, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(TypeValue, self).save(*args, **kwargs)

    def __str__(self):
        tmp = [str(self.datatype), self.value]
        return ':'.join(tmp)


class ReferenceType(_Abstract):
    """
    What kind of reference is this, e.g., dbSNP, PubMed
    """
    value = models.CharField(max_length=64)

    def __str__(self):
        return self.value


class Reference(_Abstract):
    """
    References contains PubMed number or other publications.
    reference = 8172690
    reference_type = FK 1 (PubMed)
    datatype  = FK 1 (rs12913832)
    """
    reference = models.CharField(max_length=128)
    reference_type = models.ForeignKey(ReferenceType, related_name='references')
    datatype = models.ManyToManyField(DataType, related_name='references')

    def __str__(self):
        return str(self.reference_type) + ':' + self.reference +\
               str(self.datatype.all())


class Data(_Abstract):
    """
    Data is a single bit of data from a person, for example;
    identifier    : FK 1 (Martin P. Hellwig)
    datatype  : FK 1 (rs12913832)
    value     : CG

    It is likely that at some point this table will no longer be in the RDBMS,
    but is actually in an external KeyValue store, as we will have hundreds of
    thousand data values for millions of people.
    """

    class Meta(_Abstract.Meta):
        """Override admin plural name"""
        verbose_name_plural = "Data"

    person = models.ForeignKey(Person, related_name='data')
    datatype = models.ForeignKey(DataType, related_name='data')
    value = models.TextField()

    def clean(self, *args, **kwargs):
        coercer = getattr(coercion, self.datatype.coercion.value)
        if coercer.multi_item:
            type_values = self.datatype.typevalues.all()
            test = coercer(self.value).into_string()
            values = [item.value for item in type_values]

            if test not in values:
                text = "Value '%s' must be one of: %s"
                raise ValidationError(text % (self.value, str(values)))

            self.value = test

        else:
            try:
                self.value = coercer(self.value).into_string()
            except ValueError as error_instance:
                raise ValidationError(error_instance)

        super(Data, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Data, self).save(*args, **kwargs)

    def __str__(self):
        tmp = [str(self.person), str(self.datatype), str(self.value),
               str(self.dts_insert)]
        return ':'.join(tmp)



