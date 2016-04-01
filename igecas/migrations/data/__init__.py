REFERENCETYPES = [
 'pmid']

ORIGINS = [
 'Sequence',
 'Internal',
 'Customer']

PROTOTYPES = [
 ['SNV', 'Sequence'],
 ['DIV', 'Sequence'],
 ['CUS', 'Sequence'],
 ['Derived', 'Internal'],
 ['Survey', 'Customer']]

# Find more by: http://www.ncbi.nlm.nih.gov/projects/SNV/snp_ref.cgi?rs=4341
DATATYPES = [
 ['rs1800849',  'SNV', ['A', 'G'], 'UCP3'],
 ['rs1800795',  'SNV', ['C', 'G'], 'IL6'],
 ['rs7136446',  'SNV', ['C', 'T'], 'IGF1_2'],
 ['rs6536991',  'SNV', ['C', 'T'], 'UCP1'],
 ['rs1799941',  'SNV', ['A', 'G'], 'TEST'],
 ['rs1805086',  'SNV', ['A', 'G'], 'MSTN'],
 ['rs1130214',  'SNV', ['G', 'T'], 'AKT1'],
 ['rs1801260',  'SNV', ['C', 'T'], 'CLOCK'],
 ['rs8192678',  'SNV', ['A', 'G'], 'PGC1A'],
 ['rs1801282',  'SNV', ['G', 'C'], 'PPARG'],
 ['rs9939609',  'SNV', ['A', 'T'], 'FTO'],
 ['rs4988235',  'SNV', ['C', 'T'], 'LACTOSE'],
 ['rs1799752',  'DIV', ['I', 'D'], 'ACE'],
 ['rs2228145',  'SNV', ['A', 'C'], 'IL6REC'],
 ['rs11549465', 'SNV', ['C', 'T'], 'HIF1A'],
 ['rs12913832', 'SNV', ['A', 'G'], 'BLUEEYE'],
 ['rs1805087',  'SNV', ['A', 'G'], 'MTR'],
 ['rs2854744',  'SNV', ['A', 'C'], 'IGFBP3'],
 ['rs1801131',  'SNV', ['A', 'C'], 'MTHFR'],
 ['rs1801394',  'SNV', ['A', 'G'], 'MTRR'],
 ['rs35767',    'SNV', ['A', 'G'], 'IGF1'],
 ['rs2228570',  'SNV', ['C', 'T'], 'VDR'],
 ['rs2070744',  'SNV', ['C', 'T'], 'NOS3'],
 ['rs5082',     'SNV', ['A', 'G'], 'OBES'],
 ['rs699',      'SNV', ['C', 'T'], 'AGT'],
 ['rs1815739',  'SNV', ['C', 'T'], 'ACTN3'],
 ['rs17602729', 'SNV', ['A', 'G'], 'AMPD1'],
 ['rs722208',   'SNV', ['A', 'G'], 'TEST_3'],
 ['rs1049434',  'SNV', ['A', 'T'], 'MCP'],
 ['rs2010963',  'SNV', ['C', 'G'], 'VEGFA'],
 ['rs660339',   'SNV', ['A', 'G'], 'UCP2'],
 ['rs6258',     'SNV', ['C', 'T'], 'TEST_2'],
 ['rs1799722',  'SNV', ['C', 'T'], 'BDKRB2'],
 ['rs1042713',  'SNV', ['A', 'G'], 'ADRB2'],
 ['rs662799',   'SNV', ['A', 'G'], 'APOA5'],
 ['rs762551',   'SNV', ['A', 'C'], 'CAFFEINE'],
 ['rs1800169',  'SNV', ['A', 'G'], 'CNTF'],
 ['rs4341',     'SNV', ['C', 'G'], 'ACESNV'],
 ['rs1042714',  'SNV', ['C', 'G'], 'ADRB2_2'],
 ['rs4253778',  'SNV', ['C', 'G'], 'PPARA'],
 ['rs2296135',  'SNV', ['A', 'C'], 'IL15RA'],
 ['rs2854464',  'SNV', ['A', 'G'], 'ACVR1B'],
 ['rs8111989',  'SNV', ['C', 'T'], 'CKM'],
 ['c3735GA',    'CUS', ['A', 'G'], 'MSTNRARE'],]


HEADER_REPLACE = {
 'dna \\ assay':'barcode',
 'swab id':None,
 '#upload':None,
 'ace':None,
 'actn3':None,
 'pgc1a':None,
 'ppara':None,
 'ucp2':None,
 'notes':None,
 '#comment':None,
 ':kit-datum-count':None,
 ':flags':None,
 'actn3_rs1815739':'rs1815739',
 'ucp2_rs660339':'rs660339',
 'ucp3_rs1800849':'rs1800849',
 'il6_rs1800795':'rs1800795',
 'igf1_2_rs7136446':'rs7136446',
 'ucp1_rs6536991':'rs6536991',
 'test_rs1799941':'rs1799941',
 'mstn_rs1805086':'rs1805086',
 'akt1_rs1130214':'rs1130214',
 'clock_rs1801260':'rs1801260',
 'pgc1a_rs8192678':'rs8192678',
 'pparg_rs1801282':'rs1801282',
 'fto_rs9939609':'rs9939609',
 'lactose_rs4988235':'rs4988235',
 'ace_rs1799752':'rs1799752',
 'il6rec_rs2228145':'rs2228145',
 'hif1a_rs11549465':'rs11549465',
 'blueeye_rs12913832':'rs12913832',
 'mtr_rs1805087':'rs1805087',
 'igfbp3_rs2854744':'rs2854744',
 'mthfr_rs1801131':'rs1801131',
 'mtrr_rs1801394':'rs1801394',
 'igf1_rs35767':'rs35767',
 'vdr_rs2228570':'rs2228570',
 'nos3_rs2070744':'rs2070744',
 'obes_rs5082':'rs5082',
 'agt_rs699':'rs699',
 'ampd1_rs17602729':'rs17602729',
 'test_3_rs722208':'rs722208',
 'mcp_rs1049434':'rs1049434',
 'vegfa_rs2010963':'rs2010963',
 'test_2_rs6258':'rs6258',
 'bdkrb2_rs1799722':'rs1799722',
 'adrb2_rs1042713':'rs1042713',
 'apoa5_rs662799':'rs662799',
 'caffeine_rs762551':'rs762551',
 'cntf_rs1800169':'rs1800169',
 'acesnp_rs4341':'rs4341',
 'adrb2_2_rs1042714':'rs1042714',
 'ppara_rs4253778':'rs4253778',
 'il15ra_rs2296135':'rs2296135',
 'acvr1b_rs2854464':'rs2854464',
 'ckm_rs8111989':'rs8111989',
 'c_3735ga_myostatin_rare':'c3735GA'}

from igecas import coercion

def _setup_origin(apps):
    Origin = apps.get_model('igecas', 'Origin')
    tmp = list()
    for item in ORIGINS:
        tmp.append(Origin(**{'value':item}))
        
    Origin.objects.bulk_create(tmp)
    
def _setup_prototypes(apps):
    Prototype = apps.get_model('igecas', 'Prototype')
    Origin = apps.get_model('igecas', 'Origin')
    lookup = dict()
    for entry in Origin.objects.all():
        lookup[entry.value] = entry 
    tmp = list()
    for value, origin in PROTOTYPES:
        tmp.append(Prototype(**{'value':value, 'origin':lookup[origin]}))
        
    Prototype.objects.bulk_create(tmp)

def _setup_coercion(apps):
    Coercion = apps.get_model('igecas', 'Coercion')
    tmp = list()
    for entry in dir(coercion):
        if not entry.startswith('_'):
            subject = getattr(coercion, entry)
            if issubclass(subject, coercion.FormatString):
                tmp.append(Coercion(**{'value':entry}))
    
    Coercion.objects.bulk_create(tmp)
    
def _setup_datatypes(apps):
    DataType = apps.get_model('igecas', 'DataType')
    Prototype = apps.get_model('igecas', 'Prototype')
    Coercion = apps.get_model('igecas', 'Coercion')
    
    lookup = dict()
    for entry in Prototype.objects.all():
        lookup[entry.value] = entry
        
    lookup_format = dict()
    for entry in Coercion.objects.all():
        lookup_format[entry.value] = entry

    tmp = list()
    for identifier, prototype, values, description in DATATYPES:
        coercion_format = lookup_format[coercion.FormatDualAllele.__name__]
        tmp.append(DataType(**{'identifier':identifier,
                               'description':description, 
                               'prototype':lookup[prototype],
                               'coercion':coercion_format}))
        
    DataType.objects.bulk_create(tmp)

    TypeValue = apps.get_model('igecas', 'TypeValue')
    
    lookup = dict()
    for entry in DataType.objects.all():
        lookup[entry.identifier] = entry
    
    tmp = list()
    for identifier, prototype, values, description in DATATYPES:
        datatype = lookup[identifier]
        one, two = values
        one = one.upper()
        two = two.upper()
        
        values = [one + one,
                  one + two,
                  two + two]
        
        for value in values:
            tmp.append(TypeValue(**{'value':value,
                                    'datatype':datatype,
                                    'confidence':99,
                                    }))
    
    TypeValue.objects.bulk_create(tmp)

def _setup_references(apps):
    ReferenceType = apps.get_model('igecas', 'ReferenceType')
    tmp = list()
    for item in REFERENCETYPES:
        tmp.append(ReferenceType(**{'value':item}))
        
    ReferenceType.objects.bulk_create(tmp)               
        
    
def _import():
    from igecas.models import Data, Person, DataType
    lookup = dict()
    for item in DataType.objects.all():
        lookup[item.identifier] = item
    import csv
    path = '/home/martin/git/wyatt/src/django/samples/tests/functional/workflow-steps/0060-add-kit-data.csv'
    
    tmp = list()
    with open(path) as csv_file:
        reader = csv.reader(csv_file)
        headers = None
        data_start = False

        for index, row in enumerate(reader):
            if data_start:
                values = dict(zip(headers, row))
                barcode = values['barcode']
                person, _ = Person.objects.get_or_create(identifier=barcode)
                 
                if barcode == None or barcode.strip() == '':
                    text = '# Skipping row %s because of no barcode: %s ' 
                    text = text % (index+1, values)
                    continue  
                
                for key, value in values.items():
                    if key in ['', None, 'barcode']:
                        continue
                    
                    if value == None:
                        continue
                    
                    value = value.strip().lower()
                    
                    if value == '':
                        continue
                    
                    value = value.replace('ins', 'i')
                    value = value.replace('de', 'd')
                    value = value.replace(':', '')
                    value = value.upper()
                    value = list(value)
                    value.sort()
                    value = ''.join(value)
                    
                    kwargs = {'person':person,
                              'datatype':lookup[key],
                              'value':value}

                    tmp.append(Data(**kwargs))
                

            if 'dna \\ assay' in row[0].lower().strip():
                headers = row
                
                for index, value in enumerate(headers):
                    headers[index] = HEADER_REPLACE[value.strip().lower()]
                    data_start = True
            
                
        
    Data.objects.bulk_create(tmp)

def setup_data(apps, schema_editor):
    _setup_origin(apps)
    _setup_prototypes(apps)
    _setup_coercion(apps)
    _setup_datatypes(apps)
    _setup_references(apps)
    _import()
    
